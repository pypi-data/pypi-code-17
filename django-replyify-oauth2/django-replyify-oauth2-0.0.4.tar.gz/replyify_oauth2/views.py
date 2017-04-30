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
from .models import Credentials
from .utils import store_credentials, refresh_access_token
from . import settings
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
        store_credentials(request.user, response_data)
    return redirect(request.GET.get('state', '/'))


@login_required
def refresh(request=None):
    if 'error' in request.GET:
        raise Exception(request.GET['error'])
    logger.info('** REPLYIFY: /refresh')
    try:
        next_url = request.GET.get('next', request.GET.get('state', '/'))
        request.user = refresh_access_token(request.user)
        return redirect(next_url)
    except Credentials.DoesNotExist:
        authorize(request)
