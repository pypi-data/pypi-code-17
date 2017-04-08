import asyncio
import json
import re

import aioamqp

from asynclib.amqp import logger
from asynclib.http.error import BaseError
from asynclib.utils.loop import get_event_loop


class JSONDumpError(BaseError):

    def __init__(self):
        super(JSONDumpError, self).__init__(
            code='JSON',
            description='JSON_DUMP_ERROR'
        )


class AMQPServer(object):
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
        self.endpoints = []

    def register_endpoint(self, key, endpoint):
        key = (self.prefix + self.name).replace('_', '.') + key
        pattern = '[^.]*'.join([re.escape(i) for i in key.split('*')])
        self.endpoints.append((key, re.compile(r'^{}$'.format(pattern)), endpoint))

    async def handle(self, channel, body, envelope, properties):
        for key, pattern, endpoint in self.endpoints:
            if pattern.match(envelope.routing_key):
                try:
                    message = self.dumper.loads(body)
                    result = {'result': await endpoint(**message.get('parameters', {}))}
                    if self.exchange_type != 'fanout':
                        await channel.basic_client_ack(envelope.delivery_tag)
                except BaseError as e:
                    result = {'error': e.map()}
                logger.debug('finished execution')
                if properties.reply_to is not None:
                    try:
                        body = self.dumper.dumps(result)
                    except Exception:
                        body = self.dumper.dumps({'error': JSONDumpError().map()})
                    await self.channel.basic_publish(body, exchange_name='',
                                                     routing_key=properties.reply_to,
                                                     properties={
                                                         'correlation_id': properties.correlation_id
                                                     })

    async def prepare_queues(self):
        for key, pattern, endpoint in self.endpoints:
            await self.channel.queue_bind(self.queue_name, self.exchange_name, routing_key=key)
            if self.exchange_type == 'fanout':
                await self.channel.basic_consume(self.handle, queue_name=self.queue_name, no_ack=True)
            else:
                await self.channel.basic_consume(self.handle, queue_name=self.queue_name)
            logger.debug('Endpoint %s bound to %s', key, self.queue_name)

    async def connect(self):
        self.transport, self.protocol = await aioamqp.connect(**self.credentials)
        self.channel = await self.protocol.channel()
        await self.channel.exchange_declare(self.exchange_name, self.exchange_type)
        if self.exchange_type == 'fanout':
            self.queue_name = await self.channel.queue_declare()['queue']
        else:
            await self.channel.queue_declare(self.queue_name)
        await self.channel.basic_qos(0, prefetch_count=self.prefetch_count)
        await self.prepare_queues()

    def run(self, loop):
        loop.run_until_complete(self.start())
        print("App has started")
        loop.run_forever()

    async def start(self):
        try:
            await self.connect()
        except Exception as e:
            await self.terminate()
            print('Reconnecting, in case of', e)
            await asyncio.sleep(5)
            await self.start()

    async def terminate(self):
        if self.protocol is not None:
            await self.protocol.close()
            self.transport.close()
