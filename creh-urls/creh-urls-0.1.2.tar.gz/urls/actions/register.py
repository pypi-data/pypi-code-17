# -*- coding: utf-8 -*-
from ..models import UrlRedirect
from django.core.cache import cache
from django.utils import timezone
from django.db.models import F

def update_count_views_url(url_source):
    #validate url exist in cache
    cache_url_dict = cache.get('urls_redirect')
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