# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.conf.urls import url
from .views import NotificationView

urlpatterns = [
    url(r'^notification/$', NotificationView.as_view(), name='yamoney_notification')
]
