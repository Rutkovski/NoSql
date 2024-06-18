import json

import redis

with open('/Users/d.rutkovskii/study/redis/test-data/large-file.json', 'r') as f: data = json.load(f)
r = redis.Redis(host='localhost', port=6379, db=0)

for event in data:
    event_id = event['id']
    event_type = event['type']
    public = str(event['public'])
    created_at = event['created_at']
    actor = json.dumps(event['actor'])
    repo = json.dumps(event['repo'])
    payload = json.dumps(event['payload'])

    key = f"user:{event_id}"
    r.hset(key, 'type', event_type)
    r.hset(key, 'actor', actor)
    r.hset(key, 'repo', repo)
    r.hset(key, 'payload', payload)
    r.hset(key, 'created_at', created_at)
    r.hset(public, 'public', public)
