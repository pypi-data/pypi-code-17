"""
Miscellaneous utilities.
"""
import time
from threading import Event
from threading import Thread
import traceback

from . import config


def format_exception():
    """
    Represent a traceback exception as a string in which all lines start
    with a `|` character.

    Useful for differenciating remote from local exceptions and exceptions
    that where sileced.

    Returns
    -------
    str
        A formatted string conaining an exception traceback information.
    """
    begin = '\n|>>>>>>>>'
    end = '\n|<<<<<<<<'
    return begin + '\n| '.join(traceback.format_exc().splitlines()) + end


def format_method_exception(error, method, args, kwargs):
    message = 'Error executing `%s`! (%s)\n' % (method, error)
    message += '\n> method: %s\n> args: %s\n> kwargs: %s\n' % \
        (str(method), str(args), str(kwargs))
    message += format_exception()
    return type(error)(message)


class LogLevel(str):
    """
    Identifies the log level: ERROR, WARNING, INFO, DEBUG.
    """
    def __new__(cls, value):
        if value not in ['ERROR', 'WARNING', 'INFO', 'DEBUG']:
            raise ValueError('Incorrect value "%s"!' % value)
        return super().__new__(cls, value)


def unbound_method(method):
    """
    Returns
    -------
    function
        Unbounded function.
    """
    return getattr(method.__self__.__class__, method.__name__)


def repeat(interval, action, *args):
    """
    Repeat an action forever after a given number of seconds.

    If a sequence of events takes longer to run than the time available
    before the next event, the repeater will simply fall behind.

    This function is executed in a separate thread.

    Parameters
    ----------
    interval : float
        Number of seconds between executions.
    action
        To be taken after the interval.
    args : tuple, default is ()
        Arguments for the action.

    Returns
    -------
    Event
        A timer object that can be terminated using the `stop()` method.
    """
    event = Event()

    def loop():
        while True:
            starttime = time.time()
            action(*args)
            delay = interval - (time.time() - starttime)
            if event.wait(delay):
                break

    Thread(target=loop).start()
    event.stop = event.set

    return event


def after(delay, action, *args):
    """
    Execute an action after a given number of seconds.

    This function is executed in a separate thread.

    Parameters
    ----------
    delay : float
        Number of seconds to delay the action.
    action
        To be taken after the interval.
    args : tuple, default is ()
        Arguments for the action.

    Returns
    -------
    Event
        A timer object that can be terminated using the `stop()` method.
    """
    event = Event()

    def wait():
        if event.wait(delay):
            return
        action(*args)

    Thread(target=wait).start()
    event.stop = event.set

    return event


def get_linger():
    """
    Wrapper to get the linger option from the environment variable.

    Returns
    -------
    int
        Number of seconds to linger.
        Note that -1 means linger forever.
    """
    value = config['LINGER']

    if value < 0:
        return -1
    return int(float(value) * 1000)
