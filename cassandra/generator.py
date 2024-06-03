from cassandra.cluster import Cluster
from random_words import RandomWords
import random, uuid

r = RandomWords()
cluster = Cluster()
session = cluster.connect('keyspace_test_claster')
table = 'races'

query = f"""
    INSERT INTO races (race_year, race_name, cyclist_name, rank, id)
    VALUES (%s, %s, %s, %s, %s)
    """

for i in range(1000):
    values = [random.randint(1880, 2020), r.random_word(), r.random_word(), random.randint(1, 3),
              uuid.uuid1()]
    session.execute_async(query, values)

print('all done!')
# values = [random.randint(1880, 2020), r.random_word(), r.random_word(), round(random.randint(1, 3), 1),
#               uuid.uuid1()]
# print(values)
# session.execute(query,values )
