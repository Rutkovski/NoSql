import json

import redis

with open('/Users/d.rutkovskii/study/redis/test-data/large-file.json', 'r') as f:
    data = json.load(f)
r = redis.Redis(host='localhost', port=6379, db=0)
pipe = r.pipeline()
i = 1
for user in data:
    i += 1
    pipe.zadd('user', {json.dumps(user): i})
pipe.execute()
