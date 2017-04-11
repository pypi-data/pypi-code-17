# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

DEBUG = True
SECRET_KEY = 'fake-key'
USE_TZ = True
DATABASES = dict(
    default=dict(
        ENGINE='django.db.backends.sqlite3',
        NAME=':memory:',
    ),
)
INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'yamoney',
]
ROOT_URLCONF = 'tests.urls'
ADMINS = (('Admin', 'admin@test.com'),)
YAMONEY_NOTIFICATION_SECRET = '01234567890ABCDEF01234567890'
YAMONEY_MAIL_ADMINS_ON_TRANSACTION_ERROR = True
