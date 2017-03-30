# -*- coding: utf-8 -*-

# Copyright 2017
#
# This file is part of proprietary software and use of this file
# is strictly prohibited without written consent.
#
# @author  Tim Santor  <tims@thegoco.com>

# -----------------------------------------------------------------------------

from __future__ import absolute_import, division, unicode_literals

import sys

from django.apps import apps
from django.contrib.auth.management import _get_all_permissions
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.utils.encoding import smart_unicode

# -----------------------------------------------------------------------------


class Command(BaseCommand):
    help = "Fix permissions for proxy models."

    def handle(self, *args, **options):
        for model in apps.get_models():
            opts = model._meta
            ctype, created = ContentType.objects.get_or_create(
                app_label=opts.app_label,
                model=opts.object_name.lower(),
                defaults={'name': smart_unicode(opts.verbose_name_raw)})

            for codename, name in _get_all_permissions(opts, ctype):
                p, created = Permission.objects.get_or_create(
                    codename=codename,
                    content_type=ctype,
                    defaults={'name': name})
                if created:
                    sys.stdout.write('Adding permission {}\n'.format(p))
                else:
                    sys.stdout.write('Permission {}\n'.format(p))
