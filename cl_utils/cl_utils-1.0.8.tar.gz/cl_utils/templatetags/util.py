from django.template import Library
from django.utils.translation import ugettext as _
from django.template.defaultfilters import safe
from django.utils.html import conditional_escape, escape, format_html

from math import fabs
from decimal import Decimal

register = Library()


@register.filter
def split_amount(value):
    if value:
        splitted = value.split('.') if '.' in value else value.split(',')
        if len(splitted) == 1:
            splitted.append('00')
        return '%s<span class="decimals">,%s</span>' % (escape(splitted[0]), escape(splitted[1]))
    else:
        return escape(value)
split_amount.is_safe = True


def split_data(value):
    if value:
        splitted = value.split(' ')
        return format_html('{}&nbsp;<span class="data">{}</span>', splitted[0], splitted[1])
    else:
        return escape(value)
split_data.is_safe = True
register.filter('split_data', split_data)


@register.filter
def empty(value, default=''):
    # Value can either be safe HTML or text.
    if value:
        return conditional_escape(value)
    else:
        if not default:
            default = _('empty')
        return safe("%s%s%s" % ('<span class="lighter smaller">', conditional_escape(default), '</span>'))
empty.is_safe = True


def math_absolute(value):
    return fabs(value)
register.filter('absolute', math_absolute)


@register.filter
def replace(value, arg):
    splitted = arg.split('|')

    return value.replace(splitted[0], splitted[1])

@register.filter
def multiply(value, arg):
    return Decimal(value) * Decimal(arg)


@register.filter
def divide(value, arg):
    return Decimal(value) / Decimal(arg)


@register.filter
def prettify_phonenumber(value):
    from cl_utils.utils import check_cell_phone_number
    number = check_cell_phone_number(unicode(value))
    if number is not None:
        values = {'country': number[0:3],
                  'area': number[3:6],
                  'r1': number[6:12],
                  'r2_1': number[6:8],
                  'r2_2': number[8:10],
                  'r2_3': number[10:12],
                  'r3_1': number[6:9],
                  'r3_2': number[9:12]}
        return u'%(country)s\xA0%(area)s\xA0%(r2_1)s\xA0%(r2_2)s\xA0%(r2_3)s' % values
        #return safe(u'%(country)s&nbsp;%(area)s&nbsp;%(r2_1)s&nbsp;%(r2_2)s&nbsp;%(r2_3)s' % values)
    else:
        return value


@register.filter
def prettify_trackingnumber(value):
    if not value.isdigit():
        return value

    r_value = value[::-1]
    prettified = u''

    for id, character in enumerate(r_value):
        if id % 3 == 0:
            prettified = ' ' + prettified
        prettified = character + prettified

    return prettified


@register.filter
def filesizeformat(bytes):
    """
    Formats the value like a 'human-readable' file size (i.e. 13 KB, 4.1 MB,
    102 bytes, 2047.4 MB, 2.0 GB, etc).
    """
    try:
        bytes = float(bytes)
    except (TypeError, ValueError, UnicodeDecodeError):
        bytes = 0

    if bytes == 1:
        return _('%(size)d byte') % {'size': bytes}

    if bytes < 1024:
        return _('%(size)d bytes') % {'size': bytes}
    if bytes < 1024 * 1024:
        return _('%.1f KB') % (bytes / 1024)
    # only show GB if it's on the GB or >= 10GB
    if bytes % (1024**3) == 0 or bytes > 10*1024**3:
        return _('%.1f GB') % (bytes / (1024 * 1024 * 1024))
    return _('%.1f MB') % (bytes / (1024 * 1024))
filesizeformat.is_safe = True


@register.filter
def classname(value):
    return safe(value.__class__.__name__)
classname.is_safe = True

