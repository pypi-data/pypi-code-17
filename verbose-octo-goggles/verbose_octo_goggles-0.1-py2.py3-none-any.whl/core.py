from time import time

import logging

from verbose_octo_goggles.utils import setup_logger


class SkipItem(Exception):
    pass


class StopImport(Exception):
    pass


class BaseImporter(object):
    adapter_class = None
    reader_class = None

    def __init__(self, **kwargs):
        self.type_code = kwargs.get('type_code')
        self.settings = kwargs['settings']

        self.logger = logging.getLogger(self.__class__.__name__)
        setup_logger(self.logger)

        self.adapter = self.adapter_class(importer=self)
        self.reader = self.reader_class(
            importer=self
        )

    def process(self):
        self.before_all()
        prev_finish = time()
        for item in self.reader:
            from_reader = time()
            self.logger.info('%s seconds from reader', from_reader - prev_finish)
            try:
                data = self.wrangle(item)
            except SkipItem:
                # print('skipping item', item, exc)
                self.logger.info('skipping item %s' % item)
                continue
            convert_time = time()
            self.logger.info('%s seconds to convert', convert_time - from_reader)
            self.adapter.upsert(
                data=data,
            )
            prev_finish = time()
            self.logger.info('%s seconds to db', prev_finish - convert_time)
        self.adapter.finalize()
        self.after_all()

    def wrangle(self, item):
        return item

    def before_all(self):
        self.logger.info('IMPORT START')

    def after_all(self):
        self.logger.info('IMPORT FINISH')
