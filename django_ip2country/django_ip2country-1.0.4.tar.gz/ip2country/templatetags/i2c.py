from django import template

from ip2country.utils import get_country_from_ip

register = template.Library()


@register.filter(name='ipc')
def ipc(ip):
    return get_country_from_ip(ip)

