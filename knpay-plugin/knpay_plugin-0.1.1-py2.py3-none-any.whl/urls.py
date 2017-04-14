# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf.urls import url
from knpay_plugin import views


urlpatterns = [
    url(r'^disclose/(?P<order_no>[0-9A-Za-z_\-]+)/$',
        views.DisclosureView.as_view(), name='kp_disclosure'),
    url(r'^completed/(?P<order_no>[0-9A-Za-z_\-]+)/$',
        views.BaseCompletedView.as_view(), name='kp_complete'),
]
