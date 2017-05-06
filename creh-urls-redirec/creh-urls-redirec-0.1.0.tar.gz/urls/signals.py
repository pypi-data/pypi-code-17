# -*- coding: utf-8 -*
from django.db.models.signals import post_save
from django.dispatch import receiver
from models import UrlRedirect
from django.core.cache import cache
from . import constants

@receiver(post_save, sender=UrlRedirect)
def post_save_url(sender, update_fields, instance=None, created=False,**kwargs):
    # get url_redirect (list of url)
    list_url_cache = cache.get('urls_redirect')
    # if exist delete url_redirect and url_redirect_dict
    if list_url_cache:
        cache.delete('urls_redirect')
    # get list_url_cache, url redirect active
    list_url_cache = UrlRedirect.objects.filter(status=constants.STATUS_ACTIVE).values("url_source","url_destination","date_initial_validity","date_end_validity","views")
    # create dictionary with unique index
    dict_url = {}
    for i in list_url_cache:
        dict_url[i["url_source"]]=i
    # save in cache list_url_cache and dict_url
    cache.set('urls_redirect', dict_url)
    pass