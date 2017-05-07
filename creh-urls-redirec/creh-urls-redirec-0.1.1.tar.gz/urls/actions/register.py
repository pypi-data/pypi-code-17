# -*- coding: utf-8 -*-
from ..models import UrlRedirect
from django.core.cache import cache
from django.utils import timezone
from django.db.models import F
from .. import constants

def update_count_views_url(url_source):
    #validate url exist in cache
    cache_url_dict = cache.get('urls_redirect')
    if not cache_url_dict:
        list_url_cache = UrlRedirect.objects.filter(status=constants.STATUS_ACTIVE).values("url_source",
                                                                                           "url_destination",
                                                                                           "date_initial_validity",
                                                                                           "date_end_validity", "views")
        if len(list_url_cache)>0:
            dict_url = {}
            for i in list_url_cache:
                dict_url[i["url_source"]] = i
            # save in cache list_url_cache and dict_url
            cache_url_dict = cache.get_set('urls_redirect', dict_url)


    if cache_url_dict and url_source in cache_url_dict:
        # get index
        obj = cache_url_dict[url_source]
        # validate if existe in range date
        if timezone.now()>= obj["date_initial_validity"] and \
           timezone.now() <= obj["date_end_validity"]:
            # update views in database
            UrlRedirect.objects.filter(url_source=url_source).update(views=F('views') + 1)
            return obj["url_destination"]

    return url_source