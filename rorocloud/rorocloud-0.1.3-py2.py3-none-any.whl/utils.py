import web
import logging

logger = logging.getLogger("rorocloud")


def setup_logger(verbose=False):
    if verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO
    logging.basicConfig(format='%(message)s', level=level)


def datestr(then, now=None):
    """Converts time to a human readable string.

    Wrapper over web.datestr.

        >>> from datetime import datetime
        >>> datestr(datetime(2010, 1, 2), datetime(2010, 1, 1))
        '1 day ago'
    """
    s = web.datestr(then, now)
    if 'milliseconds' in s or 'microseconds' in s:
        s = 'Just now'
    return s


def truncate(text, width):
    if len(text) > width:
        text = text[:width-3] + "..."
    return text
