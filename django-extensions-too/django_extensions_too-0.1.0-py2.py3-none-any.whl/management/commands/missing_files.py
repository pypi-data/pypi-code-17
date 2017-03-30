# -*- coding: utf-8 -*-

# Copyright 2016
#
# This file is part of proprietary software and use of this file
# is strictly prohibited without written consent.
#
# @author  Tim Santor  <tims@thegoco.com>
#
# Inspired by: https://github.com/django-extensions/django-extensions/blob/master/django_extensions/management/commands/unreferenced_files.py

# -----------------------------------------------------------------------------

import time
import os
from collections import defaultdict

from django.conf import settings
from django.db import models
from django.core.management.base import BaseCommand

# -----------------------------------------------------------------------------


def get_apps_from_cache():
    try:
        from django.apps import apps
        return [app.models_module for app in apps.get_app_configs() if app.models_module]
    except ImportError:
        from django.db.models.loading import cache
        return cache.get_apps()


def get_models_from_cache(app):
    try:
        from django.apps import apps
        return apps.get_models(app)
    except ImportError:
        from django.db.models.loading import cache
        return cache.get_models(app)

# -----------------------------------------------------------------------------


def get_exec_time(seconds):
    """Translate seconds to hh:mm:ss."""
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "%02d:%02d:%02d" % (h, m, s)


class Command(BaseCommand):
    help = "Prints a list of all files referenced in the database, but are missing in MEDIA_ROOT."

    def handle(self, *args, **options):
        start = time.time()

        file_list = []

        if settings.MEDIA_ROOT == '':
            print("MEDIA_ROOT is not set, nothing to do")
            return

        # Get list of all fields (value) for each model (key)
        # that is a FileField or subclass of a FileField
        model_dict = defaultdict(list)
        for app in get_apps_from_cache():
            for model in get_models_from_cache(app):
                for field in model._meta.fields:
                    if issubclass(field.__class__, models.FileField):
                        model_dict[model].append(field)

        # Get a list of all files missing in MEDIA_ROOT
        for model in model_dict:
            all = model.objects.all().iterator()
            for object in all:
                for field in model_dict[model]:
                    target_file = getattr(object, field.name)
                    if target_file:
                        file_list.append(target_file.path)

        # Print list of missing files
        file_list = sorted(list(set(file_list)))
        for f in file_list:
            if not os.path.exists(f):
                print(f)

        print('-' * 80)
        print('Execution time: %s' % get_exec_time(time.time()-start))
