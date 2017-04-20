import json
import logging
import pika

from assetadapter.devicemanager import DeviceManager, ScVisaError
from rpc.amqp import RpcServer

import schedule
import uuid
import datetime
import platform

schedule.run_continuously(interval=1)


def globalTick():
    print('Synchronization begins ...')

    print('Synchronization ended.')


def datetime_handler(self, x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown type")

json.JSONEncoder.default = datetime_handler

# schedule.every(10).seconds.do(globalTick)

class VisaRpcServer(RpcServer):
    def __init__(self, logger, visa_library, username, password, name='visa_rpc_server', exchange="visa_rpc",
                 host='localhost'):
        RpcServer.__init__(self, name=name, host=host, exchange=exchange, username=username, password=password)

        self.logger = logger

        self.device_manager = DeviceManager(visa_library=visa_library)

        self.create_method(name='alias', request_handler_method=self.on_alias_request)
        self.logger.info('- Registrate consumer method LOCAL.alias')

        self.create_method(name='query', request_handler_method=self.on_query_request)
        self.logger.info('- Registrate consumer method LOCAL.query')

        self.create_method(name='read', request_handler_method=self.on_read_request)
        self.logger.info('- Registrate consumer method LOCAL.read')

        self.create_method(name='write', request_handler_method=self.on_write_request)
        self.logger.info('- Registrate consumer method LOCAL.write')

        self.create_method(name='list', request_handler_method=self.on_list_request)
        self.logger.info('- Registrate consumer method LOCAL.list')

        self.create_method(name='execution', request_handler_method=self.on_execute)
        self.logger.info('- Registrate consumer method LOCAL.exec')

        self.create_method(name='close', request_handler_method=self.on_close_channel)
        self.logger.info('- Registrate consumer method LOCAL.close_channel')

        self.data_channels = []
        self.synchInterval = 3

    def on_list_request(self, ch, method, props, body):
        response = []
        try:
            request = json.loads(body.decode("utf-8"))
            response = self.device_manager.list()
            self.logger.info('LOCAL.list: ' + str(response))

        except ScVisaError as ex:
            self.logger.warning('Exception happened on LOCAL.list ' + str(ex))
            self.send_event(body={
                'error': ex.toJSON(),
                'request': body
            })
        except Exception as e:
            self.logger.error(e)
        finally:
            self.return_acknowledgement(ch=ch, method=method, props=props, response=response)

    def on_alias_request(self, ch, method, props, body):
        try:
            request = json.loads(body.decode("utf-8"))
            connected = self.device_manager.alias(request)

            response = {
                'timestamp': datetime.datetime.now(),
                'connected': connected
            }

            self.logger.info('LOCAL.alias: ' + json.dumps(request) + ' -> ' + json.dumps(response))
        except ScVisaError as ex:
            self.logger.warning('Exception happened on LOCAL.alias ' + str(ex))
            self.send_event(body={
                'error': ex.toJSON(),
                'request': body
            })

        except Exception as e:
            logging.error(e)
        finally:
            self.return_acknowledgement(ch=ch, method=method, props=props, response=json.dumps(response))

    def on_query_request(self, ch, method, props, body):
        response = {
            'timestamp': datetime.datetime.now(),
            'result': None
        }
        try:
            request = json.loads(body.decode("utf-8"))
            response['result'] = self.device_manager.query(request['alias'], request['command'])
            self.logger.info('LOCAL.query: ' + json.dumps(request) + ' -> ' + json.dumps(response)[:20] + ' ...')

        except ScVisaError as ex:
            self.logger.warning('Exception happened on LOCAL.query ' + str(ex))
            self.send_event(body={
                'error': ex.toJSON(),
                'request': body
            })
        except Exception as e:
            self.logger.error(e)
        finally:
            self.return_acknowledgement(ch=ch, method=method, props=props, response=response, headers={
                '__TypeId__': 'hu.sagax.hedgehog.visa.M2mResponse'
            })

    def on_write_request(self, ch, method, props, body):
        response = {
            'timestamp': datetime.datetime.now()
        }
        try:
            request = json.loads(body.decode("utf-8"))
            self.device_manager.write(request['alias'], request['command'])
            logging.info('LOCAL.write: ' + json.dumps(request) + ' ...')

        except ScVisaError as ex:
            self.logger.warning('Exception happened on LOCAL.write ' + str(ex))
            self.send_event(body={
                'error': ex.toJSON(),
                'request': body
            })
        except Exception as e:
            self.logger.warning('Exception happened on LOCAL.write ' + str(e))
            self.logger.error(e)
        finally:
            self.return_acknowledgement(ch=ch, method=method, props=props, response=response)

    def on_read_request(self, ch, method, props, body):
        response = {
            'timestamp': datetime.datetime.now(),
            'result': None
        }
        try:
            request = json.loads(body.decode("utf-8"))
            response['result'] = self.device_manager.read(request['alias'], request['command'])
            self.logger.info('LOCAL.read: ' + json.dumps(request) + ' -> ' + json.dumps(response)[:20] + ' ...')

        except ScVisaError as ex:
            self.logger.warning('Exception happened on LOCAL.read ' + str(ex))
            self.send_event(body={
                'error': ex.toJSON(),
                'request': body
            })
        except Exception as e:
            self.logger.error(e)
        finally:
            self.return_acknowledgement(ch=ch, method=method, props=props, response=response, headers={
                '__TypeId__': 'hu.sagax.hedgehog.visa.M2mResponse'
            })

    def on_execute(self, channel, method, props, body):
        request = json.loads(body.decode("utf-8"))
        response = {}
        # for command in request['setup']:
        try:
            self.data_channels.append(request)


            request['job'] = str(uuid.uuid4())

            response = {
                'timestamp': datetime.datetime.now(),
                'executed': True,
                'sampling': self.synchInterval,
                'domain': request['domain'],
                'job': str(uuid.uuid4()),
                'controller': platform.node()
            }

            if ('period' in request):
                schedule.every(request['period']).seconds.do(self.tick_job, request['alias'], request['domain'],
                                                             request['command']).tag(request['job'])
            else:
                schedule.every(self.synchInterval).seconds.do(self.tick_job, request['alias'], request['domain'],
                                                              request['command']).tag(request['job'])

                self.logger.info('LOCAL.execute: ' + json.dumps(
                request) + ' opened new channel with sampling in ' + str(request['period']) + ' ms.')


        except ScVisaError as ex:
            self.logger.warning('Exception happened on LOCAL.execute ' + str(ex))
            self.send_event(body={
                'error': ex.toJSON(),
                'request': body
            })

            response = {
                'timestamp': datetime.datetime.now(),
                'executed': False
            }
        except Exception as ex:
            self.logger.error(ex)

            response = {
                'timestamp': datetime.datetime.now(),
                'executed': False
            }
        finally:
            self.return_acknowledgement(ch=channel, method=method, props=props, response=response, headers={
                '__TypeId__': 'hu.sagax.hedgehog.visa.M2mStreamResponse'
            })

    def on_close_channel(self, channel, method, props, body):
        request = json.loads(body.decode("utf-8"))
        response = {}
        # for command in request['setup']:
        try:
            response['domain'] = request['domain']
            response['controller'] = platform.node()

            if ('job' in request):
                for ch in self.data_channels:
                    if ch['job'] == request['job']:
                        self.data_channels.remove(request)

                self.logger.info('LOCAL.close: ' + json.dumps(request) + ' close.')

                schedule.clear(request['job'])
                response['job'] = request['job']

            else:
                self.data_channels = []
                for job in schedule.jobs:
                    schedule.cancel_job(job)

            response['executed'] = True
            response['timestamp'] = datetime.datetime.now()

        except Exception as e:
            response={
                'timestamp': datetime.datetime.now(),
                'executed': False
            }

            self.logger.error(e)
            self.send_event(body={
                'timestamp': datetime.datetime.now(),
                'error': e,
                'request': body
            })
        finally:
            self.return_acknowledgement(ch=channel, method=method, props=props, response=response, headers={
                '__TypeId__': 'hu.sagax.hedgehog.visa.M2mStreamResponse'
            })

    def tick_job(self, alias, domain, command):
        response = {}
        try:
            response = self.device_manager.query_ascii(alias=alias, command=command).tolist()
            self.logger.info('LOCAL.query: ' + command + ' -> ' + json.dumps(response)[:20] + ' ...')
            self.send_data(alias=alias, domain=domain, timestamp=datetime.datetime.now(), value=response)
        except ScVisaError as ex:
            self.logger.warning('Exception happened on tick query ' + str(ex))
            self.send_event(body={
                'timestamp': datetime.datetime.now(),
                'error': ex.toJSON()
            })
        except Exception as ex:
            self.logger.error(ex)
            self.send_event(body={
                'timestamp': datetime.datetime.now(),
                'error': ex
            })

    def send_data(self, alias, domain, value, timestamp):
        message_properties = pika.BasicProperties(content_type='application/json', content_encoding='utf-8', headers={
            'alias': alias,
            'domain': domain,
            'controller': platform.node()
        })
        self.channel.basic_publish(
            exchange=self.exchange,
            routing_key='ingestion',
            properties=message_properties,
            body=json.dumps(obj={
                'timestamp': datetime.datetime.now(),
                'value': value
            }, ensure_ascii=False))
        self.logger.debug('Call \"' + "ingestion" + '\" request ' + str(value) + ' -> ' + str(message_properties))

    def send_event(self, body):
        message_properties = pika.BasicProperties(content_type='application/json', content_encoding='utf-8', headers={
            'controller': platform.node()
        })
        self.channel.basic_publish(
            exchange=self.exchange,
            routing_key='log',
            properties=message_properties,
            body=json.dumps(body))
        self.logger.debug('Call \"' + "log" + '\" request ' + str(body) + ' -> ' + str(message_properties))