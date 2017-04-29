#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages
from django.utils import timezone
from .models import Credentials
from . import settings
from datetime import timedelta
import requests
import urllib
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def index(request=None):
    return HttpResponse('Replyify-OAuth2 index.')


@login_required
def authorize(request=None):
    # uid = getattr(request.user, settings.REPLYIFY_USER_ID_FIELD)
    next_url = request.GET.get('next', request.GET.get('state', '/'))
    if request.GET.get('denied_redirect'):
        request.session['replyify-denied-redirect'] = request.GET['denied_redirect']
    logger.info('** REPLYIFY: /authorize - Next URL: {}'.format(next_url))
    # state = get_random_string(20, 'abcdefghijklmnopqrstuvwxyz0123456789')
    request.session['state'] = next_url
    params = {
        'client_id': settings.REPLYIFY_CLIENT_ID,
        'redirect_uri': settings.REPLYIFY_REDIRECT_URI,
        'response_type': 'code',
        'state': next_url,
    }
    url = '{0}?{1}'.format(settings.REPLYIFY_AUTH_URL, urllib.urlencode(params))
    logger.info('** REPLYIFY: /authorize - Redirecting to: {}'.format(url))
    return redirect(url)


@login_required
def callback(request=None):
    if request.GET.get('error'):
        logger.info('** REPLYIFY: /callback - Access Denied!')
        messages.error(request, request.GET.get('error').replace('_', ' ').title())
        next_url = request.session.get('replyify-denied-redirect', settings.REPLYIFY_DENIED_REDIRECT)
        logger.info('** REPLYIFY: /callback - Denied Redirect: {}'.format(next_url))
        return redirect(next_url)
    logger.info('** REPLYIFY: /callback')
    data = {
        'grant_type': 'authorization_code',
        'code': request.GET['code'],
        'client_id': settings.REPLYIFY_CLIENT_ID,
        'client_secret': settings.REPLYIFY_CLIENT_SECRET,
        'redirect_uri': settings.REPLYIFY_REDIRECT_URI
    }
    url = settings.REPLYIFY_TOKEN_URL
    logger.info('** REPLYIFY: Token URL - {}'.format(url))
    logger.info('** REPLYIFY: Token data - {}'.format(data))
    response = requests.post(url=url, data=data)
    response_data = response.json()
    logger.info('** REPLYIFY: Response data - {}'.format(response_data))
    if response_data.get('error'):
        logger.error('** REPLYIFY ERROR: {}'.format(response_data['error']))
        messages.error(request, 'REPLYIFY ERROR: {}'.format(response_data['error']))
    else:
        _store_credentials(request.user, response_data)
    return redirect(request.GET.get('state', '/'))


@login_required
def refresh(request=None):
    if 'error' in request.GET:
        raise Exception(request.GET['error'])
    logger.info('** REPLYIFY: /refresh')
    try:
        next_url = request.GET.get('next', request.GET.get('state', '/'))
        creds = Credentials.objects.get(user=request.user)

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
        _store_credentials(request.user, response.json())
        return redirect(next_url)

    except Credentials.DoesNotExist:
        authorize(request)


def _store_credentials(user, replyify_json=None):
    assert user is not None
    creds, _ = Credentials.objects.get_or_create(user=user)
    creds.access_token = replyify_json['access_token']
    creds.refresh_token = replyify_json['refresh_token']
    creds.expires = timezone.now() + timedelta(seconds=replyify_json['expires_in'])
    creds.scope = replyify_json['scope']
    creds.token_type = replyify_json['token_type']
    creds.save()
    return creds
