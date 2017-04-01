import logging
from logging import FileHandler, StreamHandler, Formatter, getLevelName
from sys import stdout
from os import makedirs
from os.path import dirname


LOGGER_FORMAT = '%(asctime)s - %(name)s:%(lineno)d - %(levelname)s - %(message)s'


def configure(config: dict):
    mode, file, level = config['mode'], config['file'], config['level']

    if mode == 'file':
        _make_log_dir(dirname(file))
        handler = FileHandler(file)
    else:
        handler = StreamHandler(stdout)

    handler.setFormatter(Formatter(LOGGER_FORMAT))
    logging.basicConfig(handlers=[handler], level=getLevelName(level))


def _make_log_dir(log_dir):
    if len(log_dir) > 0:
        makedirs(log_dir, exist_ok=True)


asterisk = logging.getLogger("contactcenter.asterisk")
worker = logging.getLogger("contactcenter.worker")
websocket = logging.getLogger("contactcenter.websocket")
controller = logging.getLogger("contactcenter.controller")
