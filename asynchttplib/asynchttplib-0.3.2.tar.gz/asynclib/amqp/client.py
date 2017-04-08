import asyncio
import json

import re
import uuid

import aioamqp
from asynclib.amqp import logger
from asynclib.http.error import BaseError


class AMQPClient(object):
    def __init__(self, name='', prefix='am', host='localhost', user='guest', password='guest',
                 vhost='/', exchange_type='topic', dumper=json, prefetch_count=1):
        if not prefix.endswith('_'):
            prefix += '_'
        if len(name) > 0 and not name.endswith('_'):
            name += '_'
        self.credentials = {
            'host': host,
            'login': user,
            'password': password,
            'virtual_host': vhost
        }
        self.dumper = dumper
        self.prefix = prefix
        self.prefetch_count = prefetch_count
        self.name = name
        self.exchange_name = self.prefix + 'exchange_' + exchange_type
        self.queue_name = self.prefix + name + 'queue_' + exchange_type
        self.transport = None
        self.protocol = None
        self.channel = None
        self.exchange_type = exchange_type
        self.waiter = asyncio.Event()
        self._reply_queue = None

    async def connect(self):
        self.transport, self.protocol = await aioamqp.connect(**self.credentials)
        self.channel = await self.protocol.channel()

    async def __aenter__(self):
        await self.connect()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    def __await__(self):
        return self.__aenter__().__await__()

    async def close(self):
        await self.protocol.close()
        self.transport.close()

    async def get_reply_queue(self):
        if self._reply_queue is None:
            self._reply_queue = (await self.channel.queue_declare(exclusive=True))['queue']
        return self._reply_queue

    async def on_reply(self, channel, body, envelope, properties):
        if properties.correlation_id == self.correlation_id:
            self.response = self.dumper.loads(body)
            self.waiter.set()

    async def call(self, key, **kwargs):
        self.correlation_id = str(uuid.uuid4())
        reply = await self.get_reply_queue()
        routing_key = (self.prefix + self.name).replace('_', '.') + key
        body = self.dumper.dumps({'parameters': kwargs})
        await self.channel.basic_consume(self.on_reply, queue_name=reply)
        await self.channel.basic_publish(body,
            self.exchange_name, routing_key=routing_key, properties={
                'correlation_id': self.correlation_id,
                'reply_to': reply
            }
        )
        await self.waiter.wait()
        if self.response.get('error') is not None:
            raise BaseError.init_with(self.response['error'])
        return self.response['result']


    async def publish(self, _name, *args, **kwargs):
        routing_key = (self.prefix + self.name).replace('_', '.') + _name
        body = self.dumper.dumps({'args': args, 'kwargs': kwargs})
        self.channel.basic_publish(body, self.exchange_name, routing_key=routing_key)
        logger.debug('Message %s with routing key %s published', body, routing_key)

