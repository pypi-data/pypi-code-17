# -*- encoding: utf-8 -*-
# ! python2

from __future__ import (absolute_import, division, print_function, unicode_literals)

from django.apps import AppConfig


class MailingAppConfig(AppConfig):
    """
    Django app config, this will set human readable name in Django admin.
    """

    name = 'django_cbtp_email'
    verbose_name = "Django CBTP e-mail"
