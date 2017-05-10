import logging
from time import time

from verbose_octo_goggles.core import SkipItem
from verbose_octo_goggles.utils import setup_logger


class BaseReader(object):
    def __init__(self, *args, **kwargs):
        self.kwargs = kwargs
        self.logger = logging.getLogger(self.__class__.__name__)
        setup_logger(self.logger)

    def __iter__(self):
        self.before_all()

        for unit in self.data_stream():
            try:
                self.before_unit(unit)
                unit = self.process_unit(unit)
                yield unit
            except SkipItem:
                self.logger.error('skipping item %s at reader', unit)
                continue

            self.after_unit(unit)
        self.after_all()

    def data_stream(self):
        raise NotImplementedError

    def process_unit(self, unit):
        return unit

    def before_all(self):
        self.counter = 0
        self.total_time = 0.0

    def after_all(self):
        self.logger.info('Total time: %s' % self.total_time)
        self.logger.info('Total actions: %s' % self.counter)

    def before_unit(self, unit):
        self.counter += 1
        self.unit_start = time()

    def after_unit(self, unit):
        self.total_time += time() - self.unit_start