#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#
from django import VERSION as DJANGO_VERSION
if DJANGO_VERSION >= (1, 7):
    default_app_config = 'replyify_oauth2.apps.ReplyifyOAuth2Config'

__version__ = '0.0.5'
