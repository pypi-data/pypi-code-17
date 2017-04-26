# -*- coding: utf-8 -*-

from unittest import TestCase
from pyramid import testing
from pyramid_view_extras import class_view_config


class BaseTest(TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_view_extras')

    def tearDown(self):
        testing.tearDown()


class TestAddClassView(BaseTest):
    def _getTargetClass(self):
        return class_view_config

    def _makeOne(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def test_create_defaults(self):
        decorator = self._makeOne()
        self.assertEqual(decorator.__dict__, {})

    def test_create_nondefaults(self):
        decorator = self._makeOne(
            name=None,
            request_type=None,
            for_=None,
            permission='foo',
            mapper='mapper',
            decorator='decorator',
            match_param='match_param'
        )
        self.assertEqual(decorator.name, None)
        self.assertEqual(decorator.request_type, None)
        self.assertEqual(decorator.for_, None)
        self.assertEqual(decorator.mapper, 'mapper')
        self.assertEqual(decorator.decorator, 'decorator')
        self.assertEqual(decorator.match_param, 'match_param')

    def test_call(self):
        pass

    def test_call_forbidden_method(self):
        pass


class TestAddResourceView(BaseTest):
    def test1(self):
        pass


class TestClassViewConfigDecorator(BaseTest):
    def test1(self):
        pass


class TestResourceViewConfigDecorator(BaseTest):
    def test1(self):
        pass
