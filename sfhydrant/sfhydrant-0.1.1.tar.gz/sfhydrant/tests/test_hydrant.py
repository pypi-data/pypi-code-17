#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2017 Red Hat
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from unittest import TestCase

from sfhydrant import hydrant

from mock import patch


class EchoBackend:
    def __init__(self):
        self.msg = None
        self.topic = None

    def add(self, msg, topic):
        self.msg = msg
        self.topic = topic
        return msg, topic


class TestHydrant(TestCase):
    def test_handler(self):
        bkd = EchoBackend()
        handler = hydrant.Hydrant(bkd)
        self.assertTrue(handler.backend == bkd)
        with patch("time.time") as t:
            t.return_value = 123456
            message = '{"a": "b"}'
            topic = 'testytest'
            handler.consume(message, topic)
            self.assertEqual({"a": "b", "TIMESTAMP": 123456}, bkd.msg)
            self.assertEqual(topic, bkd.topic)
            message = '{"a": "b", "TIMESTAMP": 23}'
            topic = 'testytest'
            handler.consume(message, topic)
            self.assertEqual({"a": "b", "TIMESTAMP": 23}, bkd.msg)
            self.assertEqual(topic, bkd.topic)
            message = '{"a": "b"}'
            topic = 'testytest/bleh'
            handler.consume(message, topic)
            self.assertEqual({"a": "b", "TIMESTAMP": 123456}, bkd.msg)
            self.assertEqual('testytest', bkd.topic)
