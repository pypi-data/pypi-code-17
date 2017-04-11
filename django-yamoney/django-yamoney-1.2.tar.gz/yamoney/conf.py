# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.conf import settings
from appconf import AppConf


class YamoneyAppConf(AppConf):
    ACCOUNT = None
    FORM_COMMENT = None
    NOTIFICATION_SECRET = ''
    MAIL_ADMINS_ON_TRANSACTION_ERROR = False
    MAIL_ADMINS_ON_TRANSACTION_ERROR_SUBJECT = 'Yamoney error'

    class Meta:
        prefix = 'YAMONEY'
