# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.test import TestCase
from django.test.utils import override_settings
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.core import mail
from .models import Transaction
from .conf import settings


class TransactionTestCase(TestCase):
    notification_url_name = 'yamoney_notification'
    test_data = {
        'notification_type': Transaction.NOTIFICATION_TYPE_P2P,
        'operation_id': '904035776918098009',
        'amount': 100,
        'withdraw_amount': 100,
        'datetime': timezone.now(),
        'sender': '41003188981230',
        'codepro': False
    }
    test_post_data = {
        'operation_id': '1234567',
        'notification_type': Transaction.NOTIFICATION_TYPE_P2P,
        'datetime': '2011-07-01T09:00:00.000+04:00',
        'sha1_hash': 'a2ee4a9195f4a90e893cff4f62eeba0b662321f9',
        'sender': '41001XXXXXXXX',
        'codepro': 'false',
        'currency': '643',
        'amount': '300.00',
        'withdraw_amount': '300.00',
        'label': 'YM.label.12345',
        'lastname': 'Иванов',
        'firstname': 'Иван',
        'fathersname': 'Иванович',
        'zip': '125075',
        'city': 'Москва',
        'street': 'Тверская',
        'building': '12',
        'suite': '10',
        'flat': '10',
        'phone': '+79253332211',
        'email': 'adress@yandex.ru',
    }

    def test_transaction_create(self):
        test_obj = Transaction.objects.create(**self.test_data)
        transaction = Transaction(**self.test_data)
        transaction.label = Transaction.generate_label(test_obj)
        transaction.save()
        self.assertEqual(transaction.get_related_obj(), test_obj)

    def test_transaction_create_view(self):
        response = self.client.post(reverse(self.notification_url_name), self.test_post_data)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(Transaction.objects.filter(operation_id=self.test_post_data['operation_id']).first())

    @override_settings(
        YAMONEY_NOTIFICATION_SECRET='invalid-secret-key'
    )
    def test_invalid_transaction_create_view(self):
        response = self.client.post(reverse(self.notification_url_name), self.test_post_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(mail.outbox), 1)
        self.assertTrue(mail.outbox[0].subject.endswith(settings.YAMONEY_MAIL_ADMINS_ON_TRANSACTION_ERROR_SUBJECT))
