#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#
from django.conf import settings

REPLYIFY_CLIENT_ID = getattr(settings, 'REPLYIFY_CLIENT_ID', None)
REPLYIFY_CLIENT_SECRET = getattr(settings, 'REPLYIFY_CLIENT_SECRET', None)
REPLYIFY_REDIRECT_URI = getattr(settings, 'REPLYIFY_REDIRECT_URI', None)

REPLYIFY_AUTH_URL = getattr(settings, 'REPLYIFY_AUTH_URL', 'https://app.replyify.com/oauth2/authorize')
REPLYIFY_TOKEN_URL = getattr(settings, 'REPLYIFY_TOKEN_URL', 'https://app.replyify.com/oauth2/token')

REPLYIFY_USER_ID_FIELD = getattr(settings, 'REPLYIFY_USER_ID_FIELD', 'id')
REPLYIFY_DENIED_REDIRECT = getattr(settings, 'REPLYIFY_DENIED_REDIRECT', '/')
