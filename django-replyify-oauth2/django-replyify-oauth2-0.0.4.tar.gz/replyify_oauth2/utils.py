#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#
from django.utils import timezone
from . import settings
from .models import Credentials
from datetime import timedelta
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def replyify_token_is_valid(user):
    try:
        return Credentials.objects.get(user=user).is_valid()
    except Credentials.DoesNotExist:
        return False


def refresh_access_token(user):
    creds = Credentials.objects.get(user=user)

    data = {
        'grant_type': 'refresh_token',
        'client_id': settings.REPLYIFY_CLIENT_ID,
        'client_secret': settings.REPLYIFY_CLIENT_SECRET,
        'refresh_token': creds.refresh_token
    }

    url = settings.REPLYIFY_TOKEN_URL
    logger.info('** REPLYIFY: Refresh Token URL - {}'.format(url))
    logger.info('** REPLYIFY: Token data - {}'.format(data))
    response = requests.post(url=url, data=data)
    user.replyify_credentials = store_credentials(user, response.json())
    return user


def store_credentials(user, replyify_json=None):
    assert user is not None
    creds, _ = Credentials.objects.get_or_create(user=user)
    creds.access_token = replyify_json['access_token']
    creds.refresh_token = replyify_json['refresh_token']
    creds.expires = timezone.now() + timedelta(seconds=replyify_json['expires_in'])
    creds.scope = replyify_json['scope']
    creds.token_type = replyify_json['token_type']
    creds.save()
    return creds
