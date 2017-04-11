# -*- coding: utf-8 -*-
# Copyright 2016-2017 LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import json
import mock
import unittest

from datetime import timedelta

from ..models.enum_user_type import EnumUserType
from ..models.enum_user_role import EnumUserRole

from ..red_october import (RedOctober,
                           RedOctoberDecryptException,
                           RedOctoberRemoteException,
                           requests,
                           )


class TestRedOctober(unittest.TestCase):

    def setUp(self):
        super(TestRedOctober, self).setUp()
        self.name = 'name'
        self.password = 'password'
        self.uses = 987
        self.owners = ['Bob', 'Charles', 'Derphead', 'Ted']
        self.labels = ['private', 'super-secure', 'definitely-tweetable']
        self.delta = timedelta(seconds=1234)
        self.delta_str = '1234s'
        self.user_type = EnumUserType['ecc']
        self.data = 'DATA'
        self.user_role = EnumUserRole['delete']
        self.data64 = self.data.encode('base64')
        self.order_num = 'AnAwesomeIdentifier!!'
        self.red_october = RedOctober('test', 1, self.name, self.password)

    def test_uri_base_https(self):
        """ It should have an HTTP URI by default """
        self.assertIn('https://', self.red_october.uri_base)

    def test_uri_base_http(self):
        """ It should have an HTTP URI if someone decides to be crazy """
        red_october = RedOctober('test', 1, '', '', ssl=False)
        self.assertIn('http://', red_october.uri_base)

    @mock.patch.object(RedOctober, 'call')
    def test_create_vault(self, call):
        """ It should call with proper args """
        self.red_october.create_vault()
        call.assert_called_once_with('create')

    @mock.patch.object(RedOctober, 'call')
    def test_delegate(self, call):
        """ It should call with proper args """
        expect = {
            'Uses': self.uses,
            'Time': self.delta_str,
        }
        self.red_october.delegate(self.delta, self.uses)
        call.assert_called_once_with('delegate', data=expect)

    @mock.patch.object(RedOctober, 'call')
    def test_create_user(self, call):
        """ It should call with proper args """
        expect = {
            'UserType': self.user_type.name.upper(),
        }
        self.red_october.create_user(self.user_type.name)
        call.assert_called_once_with('create-user', data=expect)

    @mock.patch.object(RedOctober, 'call')
    def test_get_summary(self, call):
        """ It should call with proper args """
        self.red_october.get_summary()
        call.assert_called_once_with('summary')

    @mock.patch.object(RedOctober, 'call')
    def test_encrypt(self, call):
        """ It should call with proper args """
        expect = {
            'Minimum': self.uses,
            'Owners': self.owners,
            'Data': self.data64,
        }
        self.red_october.encrypt(self.uses, self.owners, self.data)
        call.assert_called_once_with('encrypt', data=expect)

    @mock.patch.object(RedOctober, 'call')
    def test_decrypt_call(self, call):
        """ It should call with proper args """
        expect = {
            'Data': self.data64,
        }
        response = {
            'Data': self.data64,
        }
        call.return_value = json.dumps(response).encode('base64')
        self.red_october.decrypt(self.data64)
        call.assert_called_once_with('decrypt', data=expect)

    @mock.patch.object(RedOctober, 'call')
    def test_decrypt_return(self, call):
        """ It should return proper value. """
        expect = {
            'Data': self.data64,
            'Secure': True,
            'Delegates': self.owners,
        }
        call.return_value = json.dumps(expect).encode('base64')
        res = self.red_october.decrypt(self.data64)
        expect['Data'] = expect['Data'].decode('base64')
        self.assertDictEqual(res, expect)

    @mock.patch.object(RedOctober, 'call')
    def test_decrypt_fail(self, call):
        """ It should raise proper error on failure. """
        call.side_effect = RedOctoberRemoteException
        with self.assertRaises(RedOctoberDecryptException):
            self.red_october.decrypt(self.data64)

    @mock.patch.object(RedOctober, 'call')
    def test_get_owners(self, call):
        """ It should call with proper args """
        expect = {
            'Data': self.data64,
        }
        self.red_october.get_owners(self.data64)
        call.assert_called_once_with('owners', data=expect)

    @mock.patch.object(RedOctober, 'call')
    def test_get_owners_fail(self, call):
        """ It should raise proper error on failure. """
        call.side_effect = RedOctoberRemoteException
        with self.assertRaises(RedOctoberDecryptException):
            self.red_october.get_owners(self.data64)

    @mock.patch.object(RedOctober, 'call')
    def test_change_password(self, call):
        """ It should call with proper args """
        expect = {
            'NewPassword': 'new pass',
        }
        self.red_october.change_password('new pass')
        call.assert_called_once_with('password', data=expect)

    @mock.patch.object(RedOctober, 'call')
    def test_modify_user_role(self, call):
        """ It should call with proper args """
        expect = {
            'ToModify': 'Derphead',
            'Command': self.user_role.name,
        }
        self.red_october.modify_user_role('Derphead', self.user_role.name)
        call.assert_called_once_with('modify', data=expect)

    @mock.patch.object(RedOctober, 'call')
    def test_purge_delegates(self, call):
        """ It should call with proper args """
        self.red_october.purge_delegates()
        call.assert_called_once_with('purge')

    @mock.patch.object(RedOctober, 'call')
    def test_create_order(self, call):
        """ It should call with proper args """
        expect = {
            'Labels': self.labels,
            'Duration': self.delta_str,
            'Uses': self.uses,
            'Data': self.data64,
        }
        self.red_october.create_order(
            self.labels, self.delta, self.uses, self.data64,
        )
        call.assert_called_once_with('order', data=expect)

    @mock.patch.object(RedOctober, 'call')
    def test_get_orders_outstanding(self, call):
        """ It should call with proper args """
        self.red_october.get_orders_outstanding()
        call.assert_called_once_with('orderout')

    @mock.patch.object(RedOctober, 'call')
    def test_get_order_information(self, call):
        """ It should call with proper args """
        expect = {
            'OrderNum': self.order_num,
        }
        self.red_october.get_order_information(self.order_num)
        call.assert_called_once_with('orderinfo', data=expect)

    @mock.patch.object(RedOctober, 'call')
    def test_cancel_order(self, call):
        """ It should call with proper args """
        expect = {
            'OrderNum': self.order_num,
        }
        self.red_october.cancel_order(self.order_num)
        call.assert_called_once_with('ordercancel', data=expect)

    @mock.patch.object(requests, 'request')
    def test_call_request(self, requests):
        """ It should call requests with proper args """
        data = {'data': 'data',
                'Name': self.name,
                'Password': self.password,
                }
        requests_return = mock.MagicMock()
        requests.return_value = requests_return
        requests_return.json.return_value = {'Status': 'ok'}
        self.red_october.call('endpoint', 'method', 'params', data)
        requests.assert_called_once_with(
            method='method',
            url='https://test:1/endpoint',
            params='params',
            json=data,
            verify=True,
        )

    @mock.patch.object(requests, 'request')
    def test_call_error(self, requests):
        """ It should raise on non-success response """
        requests().json.return_value = {'Status': 'not ok?'}
        with self.assertRaises(RedOctoberRemoteException):
            self.red_october.call('None')

    @mock.patch.object(requests, 'request')
    def test_call_success(self, requests):
        """ It should return result on success response """
        requests().json.return_value = {'Status': 'ok',
                                        'Response': ['result']}
        res = self.red_october.call(None)
        self.assertEqual(res, ['result'])

    @mock.patch.object(requests, 'request')
    def test_call_success_bool(self, requests):
        """ It should return True on success with no response """
        requests().json.return_value = {'Status': 'ok'}
        res = self.red_october.call(None)
        self.assertTrue(res)

if __name__ == '__main__':
    unittest.main()
