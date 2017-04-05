# -*- encoding: utf-8 -*-
# Copyright 2011 Canonical Ltd.  This software is licensed under the
# GNU Affero General Public License version 3 (see the file LICENSE).

import django
from django.conf import settings
from django.core.management.base import CommandError
from django.db import DEFAULT_DB_ALIAS
from django.db.utils import load_backend


DJANGO_VERSION = django.VERSION[:2]


def check_database_engine(alias=None):
    if alias is None:
        alias = DEFAULT_DB_ALIAS

    postgresql_psycopg2_engine = load_backend(
        'django.db.backends.postgresql_psycopg2')
    engine = load_backend(settings.DATABASES[alias]['ENGINE'])
    if not issubclass(engine.DatabaseWrapper,
                      postgresql_psycopg2_engine.DatabaseWrapper):
        raise CommandError(
            'Only the postgresql_psycopg2 database engine is supported.')


def get_rolename_from_settings():
    rolename = getattr(settings, 'PG_BASE_ROLE', None)
    if rolename is None:
        raise CommandError(
            'Please provide a role name, or set the PG_BASE_ROLE setting.')
    return rolename


def parse_username_and_rolename(*args, **options):
    username = None
    rolename = None
    if DJANGO_VERSION < (1, 8):
        arg_count = len(args)

        if arg_count == 2:
            username, rolename = args
        else:
            if arg_count > 2:
                raise CommandError('Too many arguments provided.')
            elif arg_count < 1:
                raise CommandError(
                    'Please provide both a username and a role name.')
            username = args[0]
            rolename = get_rolename_from_settings()
    else:
        username = options.get('username', None)
        rolename = options.get('rolename', None)

        if isinstance(username, list) and len(username) > 0:
            username = username[0]

        if rolename is None:
            rolename = get_rolename_from_settings()

    return (username, rolename)


def parse_username(*args, **options):
    if DJANGO_VERSION < (1, 8):
        arg_count = len(args)
        if arg_count > 1:
            raise CommandError('Too many arguments provided.')
        elif arg_count < 1:
            raise CommandError('Please provide a username.')
        username = args[0]
    else:
        username = options['username']
        if isinstance(username, list) and len(username) > 0:
            username = username[0]
    return username


def parse_rolename(*args, **options):
    if DJANGO_VERSION < (1, 8):
        if len(args) < 1:
            rolename = get_rolename_from_settings()
        elif len(args) == 1:
            rolename = args[0]
        else:
            raise CommandError('Too many arguments.')
    else:
        rolename = options.get('rolename', None)
        if rolename is None:
            rolename = get_rolename_from_settings()
    return rolename


def get_models():
    try:
        from django.apps import apps
        models = apps.get_models()
    except ImportError:
        from django.db.models import loading
        models = loading.get_models()
    return models
