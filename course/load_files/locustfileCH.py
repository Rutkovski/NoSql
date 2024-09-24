import uuid
from locust import HttpUser, task, constant_pacing, events
from clickhouse_driver import Client
from locust_plugins.csvreader import CSVReader
import logging
import time
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

data_template = {
    'total_price': 77,
    'ingredients': "3 c. cut cooked chicken or turkey, 1 medium stalk celery, chopped, 1/2 c. water, 1 c. condensed cream of chicken soup, 3 1/2 c. herb seasoned croutons, 1 medium onion, 1/3 c. margarine or butter, 1 1/2 c. water",
    'link': "www.cookbooks.com/Recipe-Details.aspx?id=1045583",
    'title': "Chicken And Stuffing Bake"
}

data_reader = CSVReader("data_for_load.csv", delimiter=';', quotechar='"')


class ClickHouseClient(object):
    def __init__(self, host, username, password, database):
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.client = None
        self.connect_with_retries()

    def connect_with_retries(self, max_retries=100, delay=1):
        for attempt in range(max_retries):
            try:
                self.client = Client(host=self.host, user=self.username, password=self.password, database=self.database)
                logger.info("Connected to ClickHouse")
                return
            except Exception as e:
                logger.error(f"Connection attempt {attempt + 1} failed: {e}")
                time.sleep(delay)
        logger.error("Failed to connect to ClickHouse after 100 attempts. Exiting.")
        sys.exit(1)

    def make_query(self, query, title, type):
        start_time = time.time()
        try:
            logger.info(f"Executing query: {query}")
            result = self.client.execute(query)
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(request_type=type, name=title, response_time=total_time, response_length=0,
                                exception=None, context={}, success=True)
            logger.info(f"Query result: {result}")
            return result
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(request_type=type, name=title, response_time=total_time, response_length=0,
                                exception=e, context={}, success=False)
            logger.error(f"Query failed: {e}")
            return None


class ClickHouseUser(HttpUser):
    wait_time = constant_pacing(1)
    host = "84.201.146.138"
    login = "root"
    password = "rootPass"
    database = "default"

    def __init__(self, *args, **kwargs):
        super(ClickHouseUser, self).__init__(*args, **kwargs)
        self.client = ClickHouseClient(self.host, self.login, self.password, self.database)

    @task(100)
    def simple_select_task(self):
        row = next(data_reader)
        query = f"SELECT * FROM recipes2 WHERE id = '{uuid.UUID(row[0])}'"
        logger.info(f'Query: {query}')
        self.client.make_query(query, 'simple_select', 'select')

    # @task(25)
    # def simple_insert_and_delete_task(self):
    #     new_uuid = uuid.uuid4()
    #     insert_query = f"""
    #         INSERT INTO recipes2 (total_price, id, ingredients, link, title)
    #         VALUES ({data_template['total_price']}, '{new_uuid}', '{data_template['ingredients']}', '{data_template['link']}', '{data_template['title']}');
    #     """
    #     self.client.make_query(insert_query, 'simple_insert', 'insert')
        # delete_query = f"ALTER TABLE recipes2 DELETE WHERE total_price = {data_template['total_price']} AND id = '{new_uuid}'"
        # self.client.make_query(delete_query, 'simple_delete', 'delete')

    # @task(25)
    # def batch_insert_and_delete_task(self):
    #     uuids = [uuid.uuid4() for _ in range(100)]
    #     insert_query = """
    #         INSERT INTO recipes2 (total_price, id, ingredients, link, title)
    #         VALUES
    #     """
    #     insert_values = []
    #     for new_uuid in uuids:
    #         insert_values.append(f"({data_template['total_price']}, '{new_uuid}', '{data_template['ingredients']}', '{data_template['link']}', '{data_template['title']}')")
    #     insert_query += ", ".join(insert_values)
    #     self.client.make_query(insert_query, 'group_insert', 'insert')

        # delete_query = "ALTER TABLE recipes2 DELETE WHERE "
        # delete_conditions = []
        # for new_uuid in uuids:
        #     delete_conditions.append(f"(total_price = {data_template['total_price']} AND id = '{new_uuid}')")
        # delete_query += " OR ".join(delete_conditions)
        # self.client.make_query(delete_query, 'group_delete', 'delete')