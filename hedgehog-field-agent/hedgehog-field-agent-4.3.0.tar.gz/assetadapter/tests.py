# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import unittest

import django
import pytest

from assetadapter.tasks import list_resources, alias, read, query, write
from django.test import TestCase

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orchestrator.settings')
django.setup()


@pytest.fixture(scope='session')
def celery_config():
    return {
        'broker_url': 'amqp://',
        'result_backend': 'amqp://',
        'event_serializer': 'json',
        'result_serializer': 'json',
        'CELERY_EVENT_SERIALIZER': 'json',
        'CELERY_RESULT_SERIALIZER': 'json',
        'CELERY_ALWAYS_EAGER': True,
        'task_always_eager': True
    }


# Create your tests here.


class VisaTests(TestCase):
    # @pytest.mark.celery(result_backend='cache+memcached://127.0.0.1:11211/', serializer='json', event_serializer='json',
    #                     result_serializer='json', accept_content=['json'])
    def test_execute_task_list_resources(self):


        from assetadapter import visa_device_manager
        r = visa_device_manager.list()
        print (r)
        self.assertTrue(len(r) == 16)

    # @pytest.mark.celery(result_backend='cache+memcached://127.0.0.1:11211/', serializer='json', event_serializer='json',
    #                     result_serializer='json', accept_content=['json'])
    def test_execute_task_alias(self):
        from assetadapter import visa_device_manager

        self.assertTrue(
            visa_device_manager.alias({
                'a': 'ASRL3::INSTR',
                'c': 'USB0::0x1111::0x2222::0x4444::0::INSTR'
            }) > 0)

    # @pytest.mark.celery(result_backend='cache+memcached://127.0.0.1:11211/', serializer='json', event_serializer='json',
    #                     result_serializer='json', accept_content=['json'])
    def test_execute_task_read(self):
        from assetadapter import visa_device_manager
        visa_device_manager.alias({'a': 'ASRL1::INSTR', 'c': 'USB0::0x1111::0x2222::0x4444::0::INSTR'})
        r = visa_device_manager.read('a', '?FREQ')
        print(r)

    # @pytest.mark.celery(result_backend='cache+memcached://127.0.0.1:11211/', serializer='json', event_serializer='json',
    #                     result_serializer='json', accept_content=['json'])
    def test_execute_task_write(self):
        from assetadapter import visa_device_manager
        visa_device_manager.alias({'a': 'ASRL3::INSTR', 'c': 'USB0::0x1111::0x2222::0x4444::0::INSTR'})
        visa_device_manager.write('c', ':VOLT:IMM:AMPL 10')
        # )

    # @pytest.mark.celery(result_backend='cache+memcached://127.0.0.1:11211/', serializer='json', event_serializer='json',
    #                     result_serializer='json', accept_content=['json'])
    def test_execute_task_query(self):
        from assetadapter import visa_device_manager
        visa_device_manager.alias({'a': 'ASRL3::INSTR', 'c': 'USB0::0x1111::0x2222::0x4444::0::INSTR'})
        print(visa_device_manager.query('a', ':CURR:IMM:AMPL?'))


class CeleryVisaTests(TestCase):
    # @pytest.mark.celery(result_backend='cache+memcached://127.0.0.1:11211/', serializer='json', event_serializer='json',
    #                     result_serializer='json', accept_content=['json'])
    def test_execute_task_list_resources(self):
        r = list_resources.delay().get(timeout=10)
        print (r)
        self.assertTrue(len(r) == 16)

    # @pytest.mark.celery(result_backend='cache+memcached://127.0.0.1:11211/', serializer='json', event_serializer='json',
    #                     result_serializer='json', accept_content=['json'])
    def test_execute_task_alias(self):
        self.assertTrue(
            alias.delay({
                'a': 'ASRL3::INSTR',
                'c': 'USB0::0x1111::0x2222::0x4444::0::INSTR'
            }).get(timeout=10) > 0)

    # @pytest.mark.celery(result_backend='cache+memcached://127.0.0.1:11211/', serializer='json', event_serializer='json',
    #                     result_serializer='json', accept_content=['json'])
    def test_execute_task_read(self):
        # @celery_app.task
        # def mul(x, y):
        #     return x * y
        # alias.delay({'a': 'ASRL3::INSTR', 'c': 'USB0::0x1111::0x2222::0x4444::0::INSTR'}).get(timeout=10)
        # print(read.delay('a', ':VOLT:IMM:AMPL?').get(timeout=1))

        # alias.delay({'a': 'ASRL3::INSTR', 'c': 'USB0::0x1111::0x2222::0x4444::0::INSTR'}).get(timeout=10)
        print(read.delay('a', ':VOLT:IMM:AMPL?').get(timeout=1))

    # @pytest.mark.celery(result_backend='cache+memcached://127.0.0.1:11211/', serializer='json', event_serializer='json',
    #                     result_serializer='json', accept_content=['json'])
    def test_execute_task_write(self):
        # @celery_app.task
        # def mul(x, y):
        #     return x * y

        # assert read.delay('testasset0', 'testcommand0').get(timeout=10) != None
        # self.assertIsNone(
        alias.delay({'a': 'ASRL3::INSTR', 'c': 'USB0::0x1111::0x2222::0x4444::0::INSTR'}).get(timeout=10)
        write.delay('c', ':VOLT:IMM:AMPL 10').get(timeout=10)
        # )

    # @pytest.mark.celery(result_backend='cache+memcached://127.0.0.1:11211/', serializer='json', event_serializer='json',
    #                     result_serializer='json', accept_content=['json'])
    def test_execute_task_query(self):
        # @celery_app.task
        # def mul(x, y):
        #     return x * y
        alias.delay({'a': 'ASRL3::INSTR', 'c': 'USB0::0x1111::0x2222::0x4444::0::INSTR'}).get(timeout=10)
        print(query.delay('a', ':CURR:IMM:AMPL?').get(timeout=10,propagate=True))


def suite():
    from assetadapter.tests import VisaTests

    return unittest.TestLoader().loadTestsFromTestCase(VisaTests)

def suite():
    from assetadapter.tests import CeleryVisaTests

    return unittest.TestLoader().loadTestsFromTestCase(CeleryVisaTests)
