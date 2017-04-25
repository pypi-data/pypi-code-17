#!/usr/bin/env python
import logging.handlers


class FileLogger():
    SUPPORTED_LEVELS = ['info', 'warning', 'error']

    def __init__(self, path, **kwargs):
        self.path = path
        self.name = kwargs.get('name', 'RotatingFileLogger')
        self.is_enable_stdout = kwargs.get('stdout', True)
        self.file_counts = kwargs.get('file_counts', 0)
        self.max_file_size = kwargs.get('max_file_size', 5242880)  # 5 mb
        self.logger = self.get_file_logger()
        self._init_log_level_attributes()

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

    def _init_log_level_attributes(self):
        for level in self.SUPPORTED_LEVELS:
            setattr(self, level, lambda *args: self.log(*args, level=level))

    def log(self, *args, **kwargs):
        text = " ".join(str(string) for string in args)
        if self.is_enable_stdout:
            print(text)

        self.logger.__getattribute__(kwargs['level'])(text)

    @classmethod
    def usage(cls):
        text = """
        Module usage

        # keyword optional arguments:
        # file_counts - max file counting for the rotation
        # max_file_size - max level of content before rotating
        # name - required loggers name by native syntax. By default "RotatingFileLogger"
        # stdout - enable\disable print function call. By default "True"

        logger = FileLogger(path_to_file)
        logger.info(string)
        logger.warning(string)
        logger.warning(arg1, arg2)
        logger.error(string)

        """
        print(text)


if __name__ == '__main__':
    FileLogger.usage()
