import logging
from logging import *
from .fstring import Fmt as f

class FstringAdapter(logging.LoggerAdapter):
    def __init__(self, logger, extra={}):
        self.extra = extra
        super(FstringAdapter, self).__init__(logger, extra)
    def process(self, msg, kwargs):
        kwargs.update(self.extra)
        __lookback = kwargs.pop("__lookback",3)
        return f(msg)(__lookback=__lookback, **kwargs), kwargs
    # Convenience methods to make this act more like a Logger
    def addHandler(self, handler):
        self.logger.addHandler(handler)
    def setLevel(self, level):
        self.logger.setLevel(level)
    def removeHandler(self, hdlr):
        self.logger.removeHandler(hdlr)
    def getEffectiveLevel(self):
        return self.logger.getEffectiveLevel()
    def isEnabledFor(self, level):
        return self.isEnabledFor(level)
    def getChild(self, suffix):
        return FstringAdapter(self.logger.getChild(suffix), self.extra)

def getLogger(name=None, extra={}):
    logger = logging.getLogger(name)
    return FstringAdapter(logger,extra=extra)

class Flogging(object):
    def __init__(self):
        path = str(self.__class__).split("'")[1]
        path = path.replace("__main__.","")
        self._logger = getLogger(path, dict(__lookback=4))
    def info(self, msg, *args, **kwargs):
        self._logger.info(msg, *args, **kwargs)
    def debug(self, msg, *args, **kwargs):
        self._logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self._logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self._logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self._logger.error(msg, *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        kwargs["exc_info"] = 1
        self._logger.error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self._logger.critical(msg, *args, **kwargs)

    def log(self, level, msg, *args, **kwargs):
        self._logger.log(level, msg, *args, **kwargs)

