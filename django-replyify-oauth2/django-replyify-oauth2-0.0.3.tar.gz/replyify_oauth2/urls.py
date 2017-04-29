#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^authorize/', views.authorize, name='authorize'),
    url(r'^callback/', views.callback, name='callback'),
    url(r'^refresh/', views.refresh, name='refresh'),
    url(r'^$', views.index, name='index'),
]
