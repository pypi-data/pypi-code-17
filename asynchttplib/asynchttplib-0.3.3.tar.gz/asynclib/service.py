from aioredis import create_pool

from asynclib.amqp.server import AMQPServer
from asynclib.database.mongo import Mongo, MongoDBManager
from asynclib.http.rest import RestServer
from asynclib.utils.loop import get_event_loop


class ServiceConfig(object):
    def __init__(self, name, mongo_url='mongo://127.0.0.1', redis_host='127.0.0.1',
                 amqp_host='127.0.0.1', amqp_user='guest', amqp_password='guest'):
        self.redis_host = redis_host
        self.name = name
        self.amqp_password = amqp_password
        self.amqp_user = amqp_user
        self.amqp_host = amqp_host
        self.mongo_url = mongo_url


class Service(object):

    def __init__(self, config: ServiceConfig):
        self.config = config
        self.private_api = AMQPServer(name=self.config.name, host=self.config.amqp_host,
                                      user=self.config.amqp_user, password=self.config.amqp_password)
        self.public_api = RestServer(name=self.config.name)
        self.loop = get_event_loop()
        self._mongo = None
        self._redis = None

    @property
    def mongo(self):
        if self._mongo is None:
            self._mongo = Mongo(url=self.config.mongo_url, name=self.config.name)
        return self._mongo

    @property
    def redis(self):
        if self._redis is None:
            self._redis = create_pool((self.config.redis_host, 6379), minsize=5, maxsize=10, loop=self.loop)
        return self._redis

    def get_query_db(self, *args, **kwargs):
        return MongoDBManager(args[0], self.mongo)

    async def mongo_query(self, parameters):
        db = self.get_query_db(parameters['collection'])
        coroutine = getattr(db, parameters['method'])
        return await coroutine(*parameters.get('args', []), **parameters.get('kwargs', {}))

    def run_public_api(self, host, port):
        self.public_api.run(host=host, port=port, loop=self.loop)

    def run_private_api(self):
        self.private_api.register_endpoint('mongo', self.mongo_query)
        self.private_api.run(self.loop)