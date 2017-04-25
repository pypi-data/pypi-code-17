# mad/log.py
#
#

""" log module to set standard format of logging. """

import logging.handlers
import logging
import socket
import os

LEVELS = {
          'debug': logging.DEBUG,
          'info': logging.INFO,
          'warning': logging.WARNING,
          'warn': logging.WARNING,
          'error': logging.ERROR,
          'critical': logging.CRITICAL
         }

#:
ERASE_LINE = '\033[2K'
BOLD='\033[1m'
GRAY='\033[99m'
RED = '\033[91m'
YELLOW = '\033[93m'
GREEN = '\033[92m'
BLUE = '\033[94m'
BLA = '\033[95m'
ENDC = '\033[0m'

#:
homedir = os.path.expanduser("~")
curdir = os.getcwd()
try:
    hostname = socket.getfqdn()
except:
    hostname = "localhost"

logdir = homedir + os.sep + ".madlogs" + os.sep
logcurdir = curdir + os.sep + ".madlogs" + os.sep

#:
datefmt = '%H:%M:%S'
format_large = "%(asctime)-8s %(message)-8s %(module)s.%(lineno)s %(threadName)-10s"
format_source = "%(message)-8s %(module)s.%(lineno)-15s"
format_time = "%(asctime)-8s %(message)s"
format = "%(message)s"

class DumpHandler(logging.StreamHandler):

    def emit(self, *args, **kwargs):
        pass

class Formatter(logging.Formatter):

    def format(self, record):
        target = str(record.msg)
        if not target: target = " "
        if target[0] in [">", ]:
            target = "%s%s%s%s%s" % (BOLD, GRAY, target[0], ENDC, target[1:])
        elif target[0] in ["<", ]:
            target = "%s%s%s%s%s" % (BOLD, GRAY, target[0], ENDC, target[1:])
        elif target[0] in ["!", ]:
            target = "%s%s%s%s%s" % (BOLD, BLA, target[0], ENDC, target[1:])
        elif target[0] in ["#", ]:
            target = "%s%s%s%s" % (RED, target[0], ENDC, target[1:])
        elif target[0] in ["^", ]:
            target = "%s%s%s%s%s" % (BOLD, BLUE, target[0], ENDC, target[1:])
        elif target[0] in ["-", ]:
            target = "%s%s%s%s" % (BOLD, target[0], ENDC, target[1:])
        elif target[0] in ["&", ]:
            target = "%s%s%s%s" % (RED, target[0], ENDC, target[1:])
        record.msg = target
        return logging.Formatter.format(self, record)

class FormatterClean(logging.Formatter):

    def format(self, record):
        target = str(record.msg)
        if not target:
            target = " "
        if target[0] in [">", "<", "!", "#", "^", "-", "&"]:
            target = target[2:]
        record.msg = target
        return logging.Formatter.format(self, record)

def cdir(path):
    res = "" 
    for p in path.split(os.sep):
        res += "%s%s" % (p, os.sep)
        padje = os.path.abspath(os.path.normpath(res))
        try:
            os.mkdir(padje)
        except (IsADirectoryError, NotADirectoryError, FileExistsError):
            pass
    return True

def log(level, error):
    l = LEVELS.get(str(level).lower(), logging.NOTSET)
    logging.log(l, error)

def loglevel(loglevel="error", colors=False, dir=""):
    if dir:
        global logdir
        logdir = dir
    logger = logging.getLogger("")
    if colors:
        formatter = Formatter(format_source, datefmt=datefmt)
    else:
        formatter = FormatterClean(format_source, datefmt=datefmt)
    level = LEVELS.get(str(loglevel).lower(), logging.NOTSET)
    filehandler = None
    if not os.path.exists(logdir):
        cdir(logdir)
    if logger.handlers:
        for handler in logger.handlers:
            logger.removeHandler(handler)
    try:
        filehandler = logging.handlers.TimedRotatingFileHandler(os.path.join(logdir, "bot.log"), 'midnight')
    except Exception as ex:
        logging.error(ex)
    if filehandler:
        filehandler.setFormatter(formatter)
        filehandler.setLevel(level)
        logger.addHandler(filehandler)
    dhandler = DumpHandler()
    logger.addHandler(dhandler)        
    logger.setLevel(level)
    global enabled
    enabled = True
    return logger
