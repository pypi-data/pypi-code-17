# -*- coding: utf-8 -*-
u"""
LICENSE:
Copyright 2017 Hermann Krumrey

This file is part of kudubot-simple_responder.

    kudubot-simple_responder is an extension module for kudubot. It provides
    a Service that analyzes messages and responds to them.

    kudubot-simple_responder is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    kudubot-simple_responder is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with kudubot-simple_responder.  If not, see <http://www.gnu.org/licenses/>.
LICENSE
"""

from __future__ import absolute_import
import os
import shutil
import unittest
from kudubot.users.Contact import Contact
from kudubot.entities.Message import Message
from kudubot.tests.helpers.DummyConnection import DummyConnection
from kudubot.config.GlobalConfigHandler import GlobalConfigHandler
from kudubot.tests.helpers.backup_class_variables import prepare_class_variables_for_use
from kudubot.services.simple_responder.SimpleResponderService import SimpleResponderService


class UnitTests(unittest.TestCase):
    u"""
    Tests the Service
    """

    def setUp(self):
        u"""
        :return: None
        """
        self.restore = prepare_class_variables_for_use()
        GlobalConfigHandler.generate_configuration(False)
        self.service = SimpleResponderService(DummyConnection([SimpleResponderService]))

    def tearDown(self):
        u"""
        :return: None
        """
        self.restore()
        try:
            if os.path.isdir(u"test-kudu"):
                shutil.rmtree(u"test-kudu")
        except PermissionError:
            pass

    def test_valid_message(self):
        u"""
        Tests a valid message

        :return: None
        """

        message = Message(u"Title", u"Ping", self.service.connection.user_contact, Contact(1, u"A", u"B"))
        self.assertTrue(self.service.is_applicable_to(message))
        self.assertEqual(self.service.__check_rules__(message.message_body), u"Pong")

        self.service.connection.send_message = lambda x: self.assertTrue(x.message_body != u"")

        self.service.handle_message(message)

    def test_invalid_message(self):
        u"""
        Tests an invalid message

        :return: None
        """

        message = Message(u"Title", u"Ring", self.service.connection.user_contact, Contact(1, u"A", u"B"))
        self.assertFalse(self.service.is_applicable_to(message))
        self.assertEqual(self.service.__check_rules__(message.message_body), u"")
        self.service.handle_message(message)

        self.service.connection.send_message = lambda x: self.assertTrue(x.message_body == u"")

    def test_case_sensitive_equals(self):
        u"""
        Tests case sensitive equals rules

        :return: None
        """

        self.assertEqual(self.service.__check_rules__(u"Ping"), u"Pong")
        self.assertEqual(self.service.__check_rules__(u"PING"), u"")

    def test_case_insensitive_equals(self):
        u"""
        Tests case insensitive equals rules

        :return: None
        """

        self.assertEqual(self.service.__check_rules__(u":)"), u":) :) :)")

    def test_case_sensitive_contains(self):
        u"""
        Tests case sensitive contains rules

        :return: None
        """

        self.assertEqual(self.service.__check_rules__(u"FC Bayern"), u"Deutscher Meister 2017!")
        self.assertEqual(self.service.__check_rules__(u"FC BAyern"), u"")

    def test_case_insensitive_contains(self):
        u"""
        Tests case insensitive contains rules

        :return: None
        """

        self.assertEqual(self.service.__check_rules__(u"würfel"), u"4")
        self.assertEqual(self.service.__check_rules__(u"würFEL"), u"4")
