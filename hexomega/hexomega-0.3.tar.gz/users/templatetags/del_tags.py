from django import template

register = template.Library()


@register.filter(name='get_name')
def get_name(value):
    return value.split('/')[-1]
