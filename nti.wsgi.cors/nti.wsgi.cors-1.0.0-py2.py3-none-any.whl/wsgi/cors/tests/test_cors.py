#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904


from hamcrest import is_
from hamcrest import has_key
from hamcrest import assert_that

import unittest

from webtest import TestApp

from paste.exceptions.errormiddleware import ErrorMiddleware

from nti.wsgi.cors.cors import cors_filter_factory
from nti.wsgi.cors.cors import cors_option_filter_factory

from nti.wsgi.cors.tests import SharedConfiguringTestLayer


class TestCors(unittest.TestCase):

    layer = SharedConfiguringTestLayer

    def test_expected_exceptions_still_have_cors(self):

        def raises_app(environ, start_response):
            raise IOError('bad')

        catching_app = ErrorMiddleware(raises_app)
        app = cors_filter_factory(catching_app)

        testapp = TestApp(app)
        res = testapp.get('/the_path_doesnt_matter', status=500)

        assert_that(res.normal_body, is_(b'Failed to handle request bad'))

        # Errors set the right response headers
        res = testapp.get('/',
                          extra_environ={
                              'HTTP_ORIGIN': 'http://example.org'},
                          status=500)
        assert_that(res.headers, has_key('Access-Control-Allow-Origin'))

    def test_option_handler(self):

        def raises_app(environ, start_response):
            raise IOError('bad')

        option_app = cors_option_filter_factory(raises_app)
        app = cors_filter_factory(option_app)

        testapp = TestApp(app)
        res = testapp.options('/the_path_doesnt_matter',
                              extra_environ={
                                  'HTTP_ORIGIN': 'http://example.org'},
                              status=200)

        assert_that(res.headers, has_key('Access-Control-Allow-Methods'))

        # Non-options pass through
        res = testapp.get('/',
                          extra_environ={
                              'HTTP_ORIGIN': 'http://example.org'},
                          status=500)
        assert_that(res.headers, has_key('Access-Control-Allow-Origin'))
