import sys
import logging
import importlib
from datetime import datetime

import pytz
from six import string_types
from chardet.universaldetector import UniversalDetector

from django.utils.timezone import utc
from django.utils.translation import ungettext, ugettext as _
from django.conf import settings

_logger = None

JUST_NOW = _("just now")
SECONDS_AGO = (_("%(seconds)d second ago"), _("%(seconds)d seconds ago"))
MINUTES_AGO = (_("%(minutes)d minute ago"), _("%(minutes)d minutes ago"))
HOURS_AGO = (_("%(hours)d hour ago"), _("%(hours)d hours ago"))
YESTERDAY_AT = _("yesterday at %(time)s")
OLDER_YEAR = (_("year"), _("years"))
OLDER_MONTH = (_("month"), _("months"))
OLDER_WEEK = (_("week"), _("weeks"))
OLDER_DAY = (_("day"), _("days"))
OLDER_CHUNKS = (
    (365.0, OLDER_YEAR),
    (30.0, OLDER_MONTH),
    (7.0, OLDER_WEEK),
    (1.0, OLDER_DAY),
)
OLDER_AGO = _("%(number)d %(type)s ago")


def _un(singular__plural, n=None):
    singular, plural = singular__plural
    return ungettext(singular, plural, n)


def naturaldate(date):
    """Convert datetime into a human natural date string."""

    if not date:
        return ''

    now = datetime.now(pytz.utc)
    today = datetime(now.year, now.month, now.day, tzinfo=utc)
    delta = now - date
    delta_midnight = today - date

    days = delta.days
    hours = delta.seconds//3600
    minutes = (delta.seconds//60)%60

    if days < 0:
        return JUST_NOW

    if days == 0:
        if hours == 0:
            if int(minutes) > 0:
                return _un(MINUTES_AGO, n=minutes) % {"minutes": minutes}
            else:
                return JUST_NOW
        else:
            return _un(HOURS_AGO, n=hours) % {"hours": hours}

    if delta_midnight.days == 0:
        return YESTERDAY_AT % {"time": date.strftime("%H:%M")}

    count = 0
    for chunk, singular_plural in OLDER_CHUNKS:
        if days >= chunk:
            count = round((delta_midnight.days + 1) / chunk, 0)
            type_ = _un(singular_plural, n=count)
            break

    return OLDER_AGO % {"number": count, "type": type_}


def truncate_by_field(field, value):
    """Truncate string value by the model fields ``max_length`` attribute.

    :param field: A Django model field instance.
    :param value: The value to truncate.

    """
    if isinstance(value, string_types) and field.max_length and hasattr(field, "max_length") and len(value) > field.max_length:
        return value[:field.max_length]
    return value


def truncate_field_data(model, data):
    """Truncate all data fields for model by its ``max_length`` field
    attributes.

    :param model: Kind of data (A Django Model instance).
    :param data: The data to truncate.

    """
    fields = dict((field.name, field) for field in model._meta.fields)
    return dict((name, truncate_by_field(fields[name], value)) for name, value in data.items())


def get_default_logger():
    """Get the default logger for this application."""
    global _logger # pylint: disable=global-statement

    if _logger is None:
        _logger = logging.getLogger("feedz")
        formatter = logging.Formatter('[%(levelname)s] %(message)s')
        channel = logging.StreamHandler(stream=sys.stdout)
        channel.setFormatter(formatter)
        channel.setLevel(logging.DEBUG)
        _logger.addHandler(channel)
        _logger.setLevel(logging.DEBUG)
    return _logger

def get_encoding(filename):
    detector = UniversalDetector()
    #detector.reset()
    for line in open(filename, 'rb'):
        detector.feed(line)
        if detector.done:
            break
    detector.close()
    return detector.result

def get_article_extractor_func():
    if not settings.FEEDZ_ARTICLE_EXTRACTOR:
        return

    function_string = settings.FEEDZ_ARTICLE_EXTRACTOR
    mod_name, func_name = function_string.rsplit('.', 1)
    mod = importlib.import_module(mod_name)
    func = getattr(mod, func_name)
    result = func()
    return result
