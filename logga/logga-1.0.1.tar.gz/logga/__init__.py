__all__ = [
    "log",
    "set_console",
    "set_log_level",
    "suppress_logging",
    "enable_logging",
    "autolog",
]

import logging
import logging.config
import os
import datetime
import inspect


"""Configuration file for the logging module can be provided in the
following locations:

  * A place named by an environment variable `LOG_CONF`
  * Local directory - `./log.conf`
  * User's home directory - `~user/log.conf`

This arrangement is analogous to "rc" files.  for example, "bashrc",
"vimrc", etc.
"""

locations = [
    os.environ.get("LOG_CONF"),
    os.curdir,
    os.path.expanduser("~"),
]

found_log_config = False
for loc in locations:
    if loc is None:
        continue

    try:
        source = open(os.path.join(loc, 'log.conf'))
    except IOError as err:
        # Not a bad thing if the open failed.  Just means that the log
        # source does not exist.
        continue

    try:
        logging.config.fileConfig(source)
        source.close()
        found_log_config = True
        break
    except Exception as err:
        pass

# Holy crap!  Some black magic to identify logger handlers ...
# The calling script will be the outermost call in the stack.  Parse the
# resulting frame to get the name of the script.
logger_name = None
if found_log_config:
    s = inspect.stack()
    logger_name = os.path.basename(s[-1][1])
    if logger_name == 'nosetests' or logger_name == '<stdin>':
        logger_name = None


log = logging.getLogger(logger_name)
if logger_name is not None:
    # Contain logging to the configured handler only (not console).
    log.propagate = False

if not found_log_config:
    # If no config, just dump a basic log message to console.
    ch = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s %(levelname)s:: %(message)s")
    ch.setFormatter(formatter)
    log.addHandler(ch)
    log.level = logging.NOTSET


def set_console():
    """Drop back to the root logger handler.  This is typically the console.

    This can be used to override the logging file output stream and send
    log messages to the console.  For example, consider the following
    code that has a ``log.conf`` that writes to the log file ``my.log``::

        from logga import log, set_console
        set_console()
        log.debug('Log from inside my Python module')

    The ``set_console()`` call will force the log message to write
    ``Log from inside my Python module`` to the console.

    """
    for hdlr in log.handlers:
        log.removeHandler(hdlr)
    log.propagate = False

    ch = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s %(levelname)s:: %(message)s")
    ch.setFormatter(formatter)
    log.addHandler(ch)
    log.level = logging.NOTSET


def set_log_level(level='INFO'):
    """Set the lower threshold of logged message level.  Level
    defaults to ``INFO``.  All default log levels are supported
    ``NOTSET``, ``DEBUG``, ``INFO``, ``WARNING``, ``ERROR`` and
    ``CRITICAL`` in order of severity.

    For example::

        >>> from logga import log, set_log_level
        >>> log.debug('This DEBUG message should display')
        2014-06-30 12:50:48,407 DEBUG:: This DEBUG message should display
        >>> set_log_level(level='INFO')
        >>> log.debug('This DEBUG message should now not display')
        >>> log.debug('This DEBUG message should now not display')
        >>> log.info('This INFO message should display')
        2014-06-30 12:51:44,782 INFO:: This INFO message should display

    **Kwargs:**
        *level*: the lower log level threshold.  All log levels including
        and above this level in serverity will be logged

    """
    level_map = {
        'CRITICAL': logging.INFO,
        'ERROR': logging.INFO,
        'WARNING': logging.INFO,
        'INFO': logging.INFO,
        'DEBUG': logging.DEBUG,
        'NOTSET': logging.DEBUG,
    }

    log.setLevel(level_map[level])


def suppress_logging():
    """Provides an overriding (to level ``CRITICAL``) suppression mechanism
    for all loggers which takes precedence over the logger`s own level.

    When the need arises to temporarily throttle logging output down
    across the whole application, this function can be useful.
    Its effect is to disable all logging calls below severity level
    ``CRITICAL``.  For example::

        >>> from logga import log, suppress_logging
        >>> log.debug('This DEBUG message should display')
        2014-06-30 13:00:39,882 DEBUG:: This DEBUG message should display
        >>> suppress_logging()
        >>> log.debug('This DEBUG message should now not display')
        >>> log.critical('But CRITICAL messages will get through')
        2014-06-30 13:02:59,159 CRITICAL:: But CRITICAL messages will get through

    """
    logging.disable(logging.ERROR)


def enable_logging():
    """Opposite of the :func:`logga.suppress_logging` function.

    Re-enables logging to ``DEBUG`` level and above::

        >>> from logga import log, suppress_logging, enable_logging
        >>> suppress_logging()
        >>> log.debug('This DEBUG message should now not display')
        >>> enable_logging()
        >>> log.debug('This DEBUG message should now display')
        2014-06-30 13:08:22,173 DEBUG:: This DEBUG message should now display

    """
    logging.disable(logging.NOTSET)


def autolog(message):
    """Automatically log the current function details.

    Used interchangeably with the ``log`` handler object.  Handy for
    for verbose messaging during development by adding more verbose detail
    to the logging message, such as the calling function/method name
    and line number that raised the log call::

        >>> from logga import autolog
        >>> autolog('Verbose')
        2014-06-30 13:13:08,063 DEBUG:: Verbose: <module> in <stdin>:1
        >>> log.debug('DEBUG message')
        2014-06-30 13:15:35,319 DEBUG:: DEBUG message
        >>> autolog('DEBUG message')
        2014-06-30 13:15:41,760 DEBUG:: DEBUG message: <module> in <stdin>:1

    **Args:**
        *message*: the log message to display

    """
    if log.isEnabledFor(logging.DEBUG):
        # Get the previous frame in the stack.
        # Otherwise it would be this function!!!
        f = inspect.currentframe().f_back.f_code
        lineno = inspect.currentframe().f_back.f_lineno

        # Dump the message function details to the log.
        log.debug("%s: %s in %s:%i" % (message,
                                       f.co_name,
                                       f.co_filename,
                                       lineno))
