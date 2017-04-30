#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#
from functools import wraps
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from .models import Credentials
from .utils import refresh_access_token
import traceback


def replyify_auth_required(func):
    def decorator(func):
        def inner_decorator(request, *args, **kwargs):
            try:
                if request.user.replyify_credentials.is_valid():
                    return func(request, *args, **kwargs)
                try:
                    request.user = refresh_access_token(request.user)
                    if request.user.replyify_credentials.is_valid():
                        return func(request, *args, **kwargs)
                except Exception:
                    traceback.print_exc()
            except Credentials.DoesNotExist:
                return redirect(reverse('replyify:authorize') + '?next=' + request.GET.get('next', request.get_full_path()))
            return redirect(reverse('replyify:refresh') + '?next=' + request.GET.get('next', request.get_full_path()))
        return wraps(func)(inner_decorator)
    return decorator(func)
