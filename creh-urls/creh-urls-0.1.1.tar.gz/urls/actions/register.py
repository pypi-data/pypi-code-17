# -*- coding: utf-8 -*-
from ..models import UrlRedirect
from django.core.cache import cache
from django.utils import timezone

def update_count_views_url(url_source):
    #validate url exist in cache
    cache_url_dict = cache.get('url_redirect_dict')
    if cache_url_dict and url_source in cache_url_dict:
        # get index
        i = cache_url_dict[url_source]
        # get values of url of the index
        cache_url_dict = cache.get('url_redirect')
        # validate if existe in range date
        if timezone.now()>= cache_url_dict[i]["date_initial_validity"] and \
           timezone.now() <= cache_url_dict[i]["date_end_validity"]:
            # update views in cache
            cache_url_dict[i]["views"]=cache_url_dict[i]["views"]+1
            # update views in database
            UrlRedirect.objects.filter(url_source=url_source).update(views=cache_url_dict[i]["views"])
            # update views in cache
            cache.delete('url_redirect')
            cache.set('url_redirect',cache_url_dict)
            return cache_url_dict[i]["url_destination"]

    return url_source