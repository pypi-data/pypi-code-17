#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#
from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from django.utils import timezone


class Credentials(models.Model):
    user = models.OneToOneField(getattr(settings, 'AUTH_USER_MODEL', 'auth.User'), on_delete=models.CASCADE, related_name='replyify_credentials')
    access_token = models.CharField(max_length=50)
    refresh_token = models.CharField(max_length=50)
    expires = models.DateTimeField(default=timezone.now)
    scope = models.CharField(max_length=50)
    token_type = models.CharField(max_length=50)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        if timezone.now() > self.expires:
            return True
        return False

    def is_valid(self):
        return not self.is_expired()

    def __unicode__(self):
        return '<Replyify Creds: {}>'.format(self.access_token)
