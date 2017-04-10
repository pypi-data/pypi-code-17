#!/usr/bin/env python3

"""Thread safe gettext customizations using babel implementation"""

import threading
from collections import namedtuple

from babel.core import Locale, UnknownLocaleError
from babel.support import LazyProxy, Translations

from .core import ROOTPATH

Lang = namedtuple('Lang', 'locale trans')

_locales = {}
_data = threading.local()


def setLocale(identifier, domain='python'):
    """Set locale for current thread"""
    if (identifier, domain) in _locales:
        _data.lang = _locales[(identifier, domain)]
        return _data.lang

    try:
        locale = Locale.parse(identifier)
    except UnknownLocaleError:
        if '_' in identifier:
            _locales[(identifier, domain)] = setLocale(identifier.split('_')[0], domain)
            return _data.lang
        else:
            raise

    trans = Translations.load(str(ROOTPATH/'locale'), locale, domain)
    if not isinstance(trans, Translations) and '_' in identifier:
        _locales[(identifier, domain)] = setLocale(identifier.split('_')[0], domain)
    else:
        _data.lang = _locales[(identifier, domain)] = Lang(locale, trans)
    return _data.lang


def gettext(message):
    """Standard translation function. You can use it in all your exposed
    methods and everywhere where the response object is available.

    :parameters:
        message : Unicode
            The message to translate.

    :returns: The translated message.
    :rtype: Unicode
    """
    return _data.lang.trans.gettext(message)


def gettext_lazy(message):
    """Like ugettext, but lazy.

    :returns: A proxy for the translation object.
    :rtype: LazyProxy
    """
    def get_translation():
        """Like gettext, but lazy."""
        return _data.lang.trans.gettext(message)
    return LazyProxy(get_translation, enable_cache=False)


def ngettext(singular, plural, num):
    """Like gettext, but considers plural forms.

    :parameters:
        singular : Unicode
            The message to translate in singular form.
        plural : Unicode
            The message to translate in plural form.
        num : Integer
            Number to apply the plural formula on. If num is 1 or no
            translation is found, singular is returned.

    :returns: The translated message as singular or plural.
    :rtype: Unicode
    """
    return _data.lang.trans.ngettext(singular, plural, num)


def ngettext_lazy(singular, plural, num):
    """Like ngettext, but lazy.

    :returns: A proxy for the translation object.
    :rtype: LazyProxy
    """
    def get_translation():
        """Like ungettext, but lazy."""
        return _data.lang.trans.ngettext(singular, plural, num)
    return LazyProxy(get_translation, enable_cache=False)


def friendly_pl_date(d):
    """Quick and dirty date formatter for Polish language"""
    from datetime import date
    import dateutil.parser

    plmonths = ['stycznia', 'lutego', 'marca', 'kwietnia',
                'maja', 'czerwca', 'lipca', 'sierpnia',
                'września', 'pażdziernika', 'listopada', 'grudnia']
    if not isinstance(d, date):
        d = dateutil.parser.parse(d[:10]).date()  # pylint: disable=no-member

    return '%d %s %d' % (d.day,
                         plmonths[d.month-1],
                         d.year)


setLocale('en')
