import json

import redis

with open('/Users/d.rutkovskii/study/redis/test-data/large-file.json', 'r') as f:
    data = json.load(f)
r = redis.Redis(host='localhost', port=6379, db=0)
pipe = r.pipeline()
for user in data:
    pipe.rpush('users', json.dumps(user))
pipe.execute()