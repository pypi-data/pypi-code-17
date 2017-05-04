from django import template
from django.utils.safestring import mark_safe
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter('truncate_chars')
@stringfilter
def truncate_chars(value, max_length):
    if len(value) > max_length:
        truncd_val = value[:max_length]

        return truncd_val + u'\u2026'  #"&#x2026;"
        '''\u2026 == ellipsis'''
    
    return value
truncate_chars.is_safe=True
