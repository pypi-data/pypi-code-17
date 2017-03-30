# -*- coding: utf-8 -*-

# Copyright 2017
#
# This file is part of proprietary software and use of this file
# is strictly prohibited without written consent.
#
# @author  Tim Santor  <tims@thegoco.com>

# -----------------------------------------------------------------------------

# Django
from django.apps import apps
from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType

from django.db import connection

# -----------------------------------------------------------------------------


class Command(BaseCommand):
    """Removes all traces of an app from the DB."""

    help = "Remove an app (Must be in INSTALLED_APPS before running)"

    def add_arguments(self, parser):
        parser.add_argument('apps', nargs='+', type=str)

    def handle(self, *args, **options):
        # Get models for all apps we wish to remove
        DEL_APPS = options['apps']
        for a in DEL_APPS:
            DEL_MODELS = apps.get_app_config(a).get_models()

        # Remove Content Types
        # Removes entries from auth_permissions, djang_admin_log, django_content_type
        print('=> Remove Content Types...')
        ct = ContentType.objects.all().order_by("app_label", "model")

        for c in ct:
            if (c.app_label in DEL_APPS) or (c.model in DEL_MODELS):
                print("Deleting Content Type {} {}".format(c.app_label, c.model))
                c.delete()

        # Remove Model Tables
        print('=> Remove Model Tables...')
        for c in ct:
            if (c.app_label in DEL_APPS) or (c.model in DEL_MODELS):
                print("Deleting Table '{}_{}'".format(c.app_label, c.model))
                sql = '''
                SET FOREIGN_KEY_CHECKS=0;
                DROP TABLE {}_{};
                SET FOREIGN_KEY_CHECKS=1;'''.format(c.app_label, c.model)
                cursor = connection.cursor()
                cursor.execute(sql)

        print('=> Remove Migration History...')
        for a in DEL_APPS:
            sql = "DELETE FROM django_migrations WHERE app='{app_label}';".format(app_label=a)
            print("Deleting Migrations for app '{}'".format(a))
            cursor = connection.cursor()
            cursor.execute(sql)
