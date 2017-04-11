# coding: utf-8

from deployv.messaging.basemsg import BaseWorker
import logging

_logger = logging.getLogger('deployv')


class HttpWorker(BaseWorker):
    def __init__(self, configuration_object, sender_class, receiver_class,
                 worker_id):
        super(HttpWorker, self).__init__(configuration_object, sender_class, receiver_class,
                                         worker_id)

    def run(self):
        """ Worker method, runs the method that performs a request to the odoo controller
        and retrieves the messages
        """
        _logger.info("W%s - waiting for something to do", self._wid)
        self._receiver.run(self.callback)

    def signal_exit(self):
        """ Exit when finished with current loop """
        self._receiver.stop()

    def kill(self):
        """ This kill immediately the process, should not be used """
        self._receiver.stop()
        self.terminate()
        self.join()

    def callback(self, message):
        _logger.info('Received a message worker %s', self._wid)
        self.execute_rpc(message)
