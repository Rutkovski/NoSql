import uuid
from cassandra.auth import PlainTextAuthProvider
from locust import HttpUser, events, task, constant_pacing
from cassandra.cluster import Cluster
from cassandra.policies import RoundRobinPolicy
from cassandra.query import BatchStatement, SimpleStatement
from locust_plugins.csvreader import CSVReader
import logging
import time
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

data_template = {
    'total_price': 66.66,
    'ingredients': "3 c. cut cooked chicken or turkey, 1 medium stalk celery, chopped, 1/2 c. water, 1 c. condensed cream of chicken soup, 3 1/2 c. herb seasoned croutons, 1 medium onion, 1/3 c. margarine or butter, 1 1/2 c. water",
    'link': "www.cookbooks.com/Recipe-Details.aspx?id=1045583",
    'title': "Chicken And Stuffing Bake"
}

data_reader = CSVReader("data_for_load.csv", delimiter=';', quotechar='"')


class CassandraClient(object):
    def __init__(self, host, username, password, protocol_version=5):
        self.host = host
        self.username = username
        self.password = password
        self.session = None
        self.protocol_version = protocol_version
        self.connect_with_retries()

    def connect_with_retries(self, max_retries=100, delay=1):
        for attempt in range(max_retries):
            try:
                auth_provider = PlainTextAuthProvider(username=self.username, password=self.password)
                cluster = Cluster(contact_points=[self.host], auth_provider=auth_provider,
                                  load_balancing_policy=RoundRobinPolicy(), protocol_version=self.protocol_version)
                self.session = cluster.connect()
                logger.info("Connected to Cassandra")
                return
            except Exception as e:
                logger.error(f"Connection attempt {attempt + 1} failed: {e}")
                time.sleep(delay)
        logger.error("Failed to connect to Cassandra after 100 attempts. Exiting.")
        sys.exit(1)

    def make_query(self, query, parameters, title, type):
        start_time = time.time()
        try:
            logger.info(f"Executing query: {query} with parameters: {parameters}")
            result = self.session.execute(query, parameters)
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(request_type=type, name=title, response_time=total_time, response_length=0,
                                exception=None, context={}, success=True)
            logger.info(f"Query result: {result.all()}")
            return result
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(request_type=type, name=title, response_time=total_time, response_length=0,
                                exception=e, context={}, success=False)
            logger.error(f"Query failed: {e}")
            return None

    def execute_batch(self, batch, title, type):
        start_time = time.time()
        try:
            logger.info(f"Executing batch: {batch}")
            result = self.session.execute(batch)
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(request_type=type, name=title, response_time=total_time, response_length=0,
                                exception=None, context={}, success=True)
            logger.info(f"Batch result: {result.all()}")
            return result
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(request_type=type, name=title, response_time=total_time, response_length=0,
                                exception=e, context={}, success=False)
            logger.error(f"Batch failed: {e}")
            return None


class CassandraUser(HttpUser):
    wait_time = constant_pacing(1)
    host = "84.201.146.138"
    login = "root"
    password = "rootPass"

    def __init__(self, *args, **kwargs):
        super(CassandraUser, self).__init__(*args, **kwargs)
        self.client = CassandraClient(self.host, self.login, self.password)

    @task(76)
    def simple_select_task(self):
        row = next(data_reader)
        query = 'SELECT * FROM my_keyspace.recipes5 WHERE id = %s'
        logger.info(f'Query: {query}')
        parameters = (uuid.UUID(row[0]),)
        self.client.make_query(query, parameters, 'simple_select', 'select')

    @task(12)
    def simple_insert_and_delete_task(self):
        new_uuid = uuid.uuid4()
        insert_query = """
                    INSERT INTO my_keyspace.recipes5 (total_price, id, ingredients, link, title)
                    VALUES (%s, %s, %s, %s, %s);
                """
        insert_parameters = (
            data_template['total_price'],
            new_uuid,
            data_template['ingredients'],
            data_template['link'],
            data_template['title']
        )
        self.client.make_query(insert_query, insert_parameters, 'simple_insert', 'insert')
        delete_query = "DELETE FROM my_keyspace.recipes5 WHERE total_price = %s AND id = %s;"
        delete_parameters = (data_template['total_price'], new_uuid)
        self.client.make_query(delete_query, delete_parameters, 'simple_delete', 'delete')

    @task(12)
    def batch_insert_and_delete_task(self):
        batch = BatchStatement()
        uuids = [uuid.uuid4() for _ in range(100)]

        for new_uuid in uuids:
            insert_query = SimpleStatement("""
                INSERT INTO my_keyspace.recipes5 (total_price, id, ingredients, link, title)
                VALUES (%s, %s, %s, %s, %s);
            """)
            insert_parameters = (
                data_template['total_price'],
                new_uuid,
                data_template['ingredients'],
                data_template['link'],
                data_template['title']
            )
            batch.add(insert_query, insert_parameters)

        self.client.execute_batch(batch, 'batch_insert', 'insert')
        batch.clear()

        for new_uuid in uuids:
            delete_query = SimpleStatement("DELETE FROM my_keyspace.recipes5 WHERE total_price = %s AND id = %s;")
            delete_parameters = (data_template['total_price'], new_uuid)
            batch.add(delete_query, delete_parameters)
        self.client.execute_batch(batch, 'batch_delete', 'delete')
