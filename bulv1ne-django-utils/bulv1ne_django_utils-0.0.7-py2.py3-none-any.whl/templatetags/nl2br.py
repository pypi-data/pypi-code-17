from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(is_safe=True)
def nl2br(obj):
    return mark_safe('<br/>'.join(obj.split('\n')))
