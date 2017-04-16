#!/usr/bin/env python
import logging.handlers


class FileLogger():
    def __init__(self, name, path, **kwargs):
        self.name = name
        self.path = path
        self.file_counts = kwargs.get('file_counts') or 0
        self.max_file_size = kwargs.get('max_file_size') or 5242880  # 5 mb
        self.logger = self.get_file_logger()
        self.info = lambda text: self.logger.info(text)
        self.warning = lambda text: self.logger.warning(text)
        self.error = lambda text: self.logger.error(text)

    def get_file_logger(self):
        logger = logging.getLogger(self.name)
        logger.setLevel(logging.DEBUG)
        handler = logging.handlers.RotatingFileHandler(
            self.path,
            maxBytes=self.max_file_size,
            backupCount=self.file_counts,
        )
        formatter = logging.Formatter('%(asctime)s:%(levelname)s: %(message)s')
        handler.setFormatter(formatter)
        handler.setLevel(logging.DEBUG)
        logger.addHandler(handler)
        return logger

    @classmethod
    def usage(cls):
        text = """
        Module usage

        # keyword optional arguments:
        # file_counts - max file counting for the rotation
        # max_file_size - max level of content before rotating
        logger = FileLogger(name, path_to_file)
        logger.info(text)
        logger.warning(text)
        logger.error(text)

        """
        print(text)


if __name__ == '__main__':
    FileLogger.usage()
