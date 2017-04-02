import json


class RedisObjectCache(object):

    def __init__(self, redis, object_prefix):
        self.redis = redis
        self.object_prefix = object_prefix

    async def set(self, obj, _id):
        await self.redis.execute('set', '{}{}.'.format(self.object_prefix, _id), json.dumps(obj))

    async def get(self, _id):
         return json.loads(await self.redis.execute('get', '{}{}.'.format(self.object_prefix, _id)))