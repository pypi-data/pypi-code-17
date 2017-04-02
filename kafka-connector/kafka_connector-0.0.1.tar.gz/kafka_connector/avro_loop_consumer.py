# -*- coding: utf-8 -*-

import logging

from confluent_kafka.avro import AvroConsumer

__author__ = u'Stephan Müller'
__copyright__ = u'2017, Stephan Müller'
__license__ = u'MIT'

logger = logging.getLogger(__name__)

default_conf = {
    'log_level': 0,
    'api.version.request': True,
}


class AvroLoopConsumer(AvroConsumer):

    """
    
    The default config is
    
    >>> default_conf = {    
    ...    'log_level': 0,
    ...    'api.version.request': True,
    ...  }    
    
    """

    def __init__(self, bootstrap_servers, schema_registry_url, consumer_group, topics, config=default_conf,
                 error_callback=lambda err: AvroLoopConsumer.error_callback(err)):
        """

        :param bootstrap_servers: 
        :type bootstrap_servers: str
        :param schema_registry_url: 
        :type schema_registry_url: str
        :param topics: List of topics (strings) to subscribe to. Regexp pattern subscriptions are supported by prefixing
            the topic string with ``"^"``, e.g. ``["^my_topic.*", "^another[0-9]-?[a-z]+$", "not_a_regex"]``
        :type topics: list(str) 
        :param config: 
        :type config: dict
        :param error_callback: function that handles occurring error events
        :type error_callback: lambda err: function(err)
        """

        self._topics = topics
        self._config = config

        if error_callback is not None:
            self._config.update({"error_cb": error_callback})

        self._config['bootstrap.servers'] = bootstrap_servers
        self._config['schema.registry.url'] = schema_registry_url
        self._config['group.id'] = consumer_group

        super().__init__(self._config)

        super().subscribe(self._topics)

        self._started = False
        self._running = False
        self._stopped = False

    def loop(self, on_delivery, timeout=None):
        """
        Consumes and decodes Avro messages from kafka
        
        :param on_delivery: function that handles successful received and decoded messages
        :type on_delivery: lambda msg: function(msg)
        :param timeout: Maximum time to block waiting for message, event or callback
        :type timeout: float
        """

        if not callable(on_delivery):
            raise AttributeError("on_delivery is not callable")

        self._started = True
        self._running = True
        while self._running:
            msg = super().poll(timeout)
            if msg is None:
                logger.info("poll() timeout")
            elif msg.error():
                if msg.error().str() != "Broker: No more messages":
                    logger.info(msg.error().str())
            else:
                logger.info("Received message from topic '%s' with offset %s"
                            % (str(msg.topic()), str(msg.offset())))
                on_delivery(msg)


        super().close()
        self._stopped = True

    def stop(self):
        self._running = False

    def is_stopped(self):
        """
        :return: ``True``, if consumer loop finished
        :rtype: bool
        """
        return self._stopped

    @staticmethod
    def on_delivery(err, msg):
        if err is not None:
            logger.error(str(err))
        else:
            logger.info("Delivered message with topic '%s' with offset '%s' successfully"
                        % (str(msg.topic()), str(msg.offset())))

    @staticmethod
    def error_callback(err):
        logger.error(str(err))
