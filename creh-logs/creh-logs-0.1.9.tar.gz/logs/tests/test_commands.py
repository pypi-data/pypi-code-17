# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.management import call_command

from django.test import TestCase

from ..actions import register
from .. import contstants
from ..models import Log


class ActionsTestCase(TestCase):

    def setUp(self):
        self.create_logs()

    def create_logs(self):
        register.create_log(title='Log 1 title', message='Test error 1', location='test.py')
        register.create_log(title='Log 2 title', message='Test error 1', location='test.py')
        register.create_log(title='Log 3 title', message='Test error 1', location='test.py')

    def test_archived_logs(self):
        log_archived = Log.objects.filter(status=contstants.STATUS_ARCHIVED)
        log_actives = Log.objects.filter(status=contstants.STATUS_ACTIVE)

        self.assertEquals(log_archived.count(), 0)
        self.assertEquals(log_actives.count(), 3)

        args = []
        opts = {}
        call_command('archived_logs', *args, **opts)

        log_archived = Log.objects.filter(status=contstants.STATUS_ARCHIVED)
        log_actives = Log.objects.filter(status=contstants.STATUS_ACTIVE)

        self.assertEquals(log_archived.count(), 3)
        self.assertEquals(log_actives.count(), 0)

    def test_clean_logs(self):
        Log.objects.all().update(status=contstants.STATUS_ARCHIVED)

        log_archived = Log.objects.filter(status=contstants.STATUS_ARCHIVED)
        log_deleted = Log.objects.filter(status=contstants.STATUS_DELETED)

        self.assertEquals(log_archived.count(), 3)
        self.assertEquals(log_deleted.count(), 0)

        args = []
        opts = {}
        call_command('delete_logs', *args, **opts)

        log_archived = Log.objects.filter(status=contstants.STATUS_ARCHIVED)
        log_actives = Log.objects.filter(status=contstants.STATUS_ACTIVE)

        self.assertEquals(log_archived.count(), 0)
        self.assertEquals(log_actives.count(), 0)
