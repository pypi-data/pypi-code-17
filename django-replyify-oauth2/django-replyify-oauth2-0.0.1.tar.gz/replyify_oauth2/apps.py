#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#
from __future__ import unicode_literals
from django import VERSION as DJANGO_VERSION

if DJANGO_VERSION >= (1, 7):
    from django.apps import AppConfig

    class ReplyifyOAuth2Config(AppConfig):
        name = 'replyify_oauth2'
        verbose_name = 'Replyify OAuth2'
        label = 'replyify_oauth2'
