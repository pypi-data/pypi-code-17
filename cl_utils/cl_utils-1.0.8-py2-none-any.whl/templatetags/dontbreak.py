from django import template
from django.utils.safestring import mark_safe
import re
from cgi import escape

register = template.Library()

@register.filter
def dontbreak(value):
    """
    Replace spaces with &nbsp;
    """

    value = escape(value).replace(' ', '&nbsp;')

    return mark_safe(value)
dontbreak.is_safe = True
