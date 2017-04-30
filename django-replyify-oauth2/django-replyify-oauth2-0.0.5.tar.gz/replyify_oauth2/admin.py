#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#
from django.contrib import admin
from django.contrib.auth import get_user_model
from . import settings
from .models import Credentials


def user_search_fields():
    User = get_user_model()
    USERNAME_FIELD = getattr(User, 'USERNAME_FIELD', None)
    fields = []
    if USERNAME_FIELD is not None:
        # Using a Django 1.5+ User model
        fields = [
            'user__{}'.format(USERNAME_FIELD),
            'user__{}'.format(settings.REPLYIFY_USER_ID_FIELD)
        ]
    return fields


class CredentialsAdmin(admin.ModelAdmin):
    search_fields = ['access_token'] + user_search_fields()
    raw_id_fields = ('user',)


admin.site.register(Credentials, CredentialsAdmin)
