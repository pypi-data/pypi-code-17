"""This module implements event logging.

Event logging is implemented via *@log_event* and *@log_exception* decorators.

Logging level is configured via *loglevel* parameter in configuration file, which may take one of the following values:

* INFO
* ERROR
* DEBUG

Default loglevel is **ERROR**. With this loglevel, exceptions are logged with request URL and response code, no sensitive
information is logged. 

A path and file name of the logfile is defined by *logfile* parameter in configuration file which takes full absolute
path and filename to configuration file. Default logfile location is **pyvdp.log** in the same directory, where 
configuration file is located.

**Usage:**

    ..  code-block:: python
    
        from pyvdp import logger
        
        @logger.log_event
        def foo(bar):
            return baz
            
        @logger.log_exception
        def xyz(abc):
            return True
"""
import functools
import logging
import uuid

from pyvdp import configuration

config = configuration.get_config()


def get_logger():
    """Creates an instance of logger.
    
    :return: logger 
    """
    logger = logging.getLogger('pyvdp')
    loglevel = logging.getLevelName(config['loglevel'])
    logger.setLevel(loglevel)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    if not logger.handlers:
        fh = logging.FileHandler(config['logfile'])
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger


def log_event(func):
    """Decorator function to log events."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger = get_logger()

        result = func(*args, **kwargs)

        _uuid = uuid.uuid4()

        logger.info("[%s] Request: %s %s" % (_uuid, result['request']['method'], result['request']['url']))
        logger.debug("[%s] Request HTTP headers: %s" % (_uuid, result['request']['headers']))
        logger.debug("[%s] Request payload: %s" % (_uuid, result['request']['body']))

        logger.info("[%s] Response: HTTP %s" % (_uuid, result['response']['code']))
        logger.debug("[%s] Response HTTP headers: %s" % (_uuid, result['response']['headers']))
        logger.debug("[%s] Response message: %s" % (_uuid, result['response']['message']))

        return result

    return wrapper


def log_exception(func):
    """Decorator function to log exceptions."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger = get_logger()

        result = kwargs['result']

        _uuid = uuid.uuid4()

        logger.error("[%s] Request: %s %s" % (_uuid, result['request']['method'], result['request']['url']))
        logger.debug("[%s] Request headers: %s" % (_uuid, result['request']['headers']))
        logger.debug("[%s] Request payload: %s" % (_uuid, result['request']['body']))

        logger.error("[%s] Response: HTTP %s" % (_uuid, result['response']['code']))
        logger.debug("[%s] Response headers: %s" % (_uuid, result['response']['headers']))
        logger.debug("[%s] Response message: %s" % (_uuid, result['response']['message']))

        func(*args, **kwargs)

    return wrapper
