# -*- coding: utf-8 -*-
"""Test API class."""

# python imports
import requests
import responses

# local imports
from mls.apiclient import api, exceptions
from mls.apiclient.tests import base, utils


class TestAPI(base.BaseTestCase):
    """API test case."""
    PATH = '/api/rest/v1/developments'

    def setUp(self):
        responses.start()
        self.api = self._callFUT(self.BASE_URL)

    def tearDown(self):
        responses.stop()
        responses.reset()

    def _callFUT(self, base_url, api_key=None, lang=None, debug=False):
        return api.API(base_url, api_key=api_key, lang=lang, debug=debug)

    def test_class(self):
        """Validate the class initialization and attributes."""
        api = self._callFUT(
            self.BASE_URL,
            api_key='1234567890abcdef',
            lang='de',
            debug=True,
        )
        self.assertEqual(api.base_url, self.BASE_URL)
        self.assertEqual(api.api_key, '1234567890abcdef')
        self.assertEqual(api.lang, 'de')
        self.assertTrue(api.debug)

    def test_headers(self):
        """Validate the ``headers`` method."""
        headers = self.api.headers()
        self.assertEqual(len(headers.keys()), 2)
        self.assertEqual(headers['Content-Type'], 'application/json')
        self.assertEqual(headers['Accept'], 'application/json')

    def test_handle_http_response_200(self):
        """Validate a HTTP 200 code."""
        content = u'{"some": "content"}'
        responses.add(
            responses.GET,
            self.URL,
            status=200,
        )
        response = requests.get(self.URL)
        result = self.api.handle_response(response, content)
        data = result.get('response')
        self.assertEqual(data, {'some': 'content'})

        result = self.api.handle_response(response, None)
        data = result.get('response')
        self.assertEqual(data, {})

        self.assertRaises(
            ValueError,
            self.api.handle_response, response, u'No JSON',
        )

    def test_handle_api_response_200(self):
        """Validate a API 200 code."""
        content = utils.wrap_content(u'{"some": "content"}', status_code=200)
        responses.add(
            responses.GET,
            self.URL,
            body=content,
            status=200,
        )
        response = requests.get(self.URL)
        result = self.api.handle_response(response, content)
        data = result.get('response')
        self.assertEqual(data, {'some': 'content'})

    def test_handle_http_response_30x(self):
        """Validate a HTTP 30x code."""
        responses.add(
            responses.GET,
            self.URL,
            status=301,
        )
        response = requests.get(self.URL)
        self.assertRaises(
            exceptions.Redirection,
            self.api.handle_response, response, None,
        )

    def test_handle_api_response_30x(self):
        """Validate a API 30x code."""
        content = utils.wrap_content(u'"Redirect"', status_code=301)
        responses.add(
            responses.GET,
            self.URL,
            body=content,
            status=200,
        )
        response = requests.get(self.URL)
        self.assertRaises(
            exceptions.Redirection,
            self.api.handle_response, response, content,
        )

    def test_handle_http_response_400(self):
        """Validate a HTTP 400 code."""
        responses.add(
            responses.GET,
            self.URL,
            status=400,
        )
        response = requests.get(self.URL)
        self.assertRaises(
            exceptions.BadRequest,
            self.api.handle_response, response, None,
        )

    def test_handle_api_response_400(self):
        """Validate a API 400 code."""
        content = utils.wrap_content(u'"Bad request"', status_code=400)
        responses.add(
            responses.GET,
            self.URL,
            body=content,
            status=200,
        )
        response = requests.get(self.URL)
        self.assertRaises(
            exceptions.BadRequest,
            self.api.handle_response, response, content,
        )

    def test_handle_http_response_401(self):
        """Validate a HTTP 401 code."""
        responses.add(
            responses.GET,
            self.URL,
            status=401,
        )
        response = requests.get(self.URL)
        self.assertRaises(
            exceptions.UnauthorizedAccess,
            self.api.handle_response, response, None,
        )

    def test_handle_api_response_401(self):
        """Validate a API 401 code."""
        content = utils.wrap_content(u'"Unauthorized access"', status_code=401)
        responses.add(
            responses.GET,
            self.URL,
            body=content,
            status=200,
        )
        response = requests.get(self.URL)
        self.assertRaises(
            exceptions.UnauthorizedAccess,
            self.api.handle_response, response, content,
        )

    def test_handle_http_response_500(self):
        """Validate a HTTP 500 code."""
        responses.add(
            responses.GET,
            self.URL,
            status=500,
        )
        response = requests.get(self.URL)
        self.assertRaises(
            exceptions.ServerError,
            self.api.handle_response, response, None,
        )

    def test_handle_api_response_500(self):
        """Validate a API 500 code."""
        content = utils.wrap_content(u'"Server Error"', status_code=500)
        responses.add(
            responses.GET,
            self.URL,
            body=content,
            status=200,
        )
        response = requests.get(self.URL)
        self.assertRaises(
            exceptions.ServerError,
            self.api.handle_response, response, content,
        )

    def test_get(self):
        """Validate the ``get`` method."""
        content = u'{"some": "content"}'
        responses.add(
            responses.GET,
            self.URL,
            body=content,
            status=200,
        )
        result = self.api.get(self.PATH)
        data = result.get('response')
        self.assertEqual(data, {'some': 'content'})

    def test_http_call(self):
        """Validate the ``http_call`` method."""
        content = u'{"some": "content"}'
        responses.add(
            responses.GET,
            self.URL,
            body=content,
            status=200,
        )
        result = self.api.http_call(self.URL, 'GET')
        data = result.get('response')
        self.assertEqual(data, {'some': 'content'})

    def test_request(self):
        """Validate the ``request`` method."""
        responses.add(
            responses.GET,
            self.URL,
            body='',
            status=200,
        )
        result = self.api.request(self.URL, 'GET')
        data = result.get('response')
        self.assertEqual(data, {})

        # Reset responses here to test same URL with different content.
        responses.reset()

        content = u'{"some": "content"}'
        responses.add(
            responses.GET,
            self.URL,
            body=content,
            status=200,
        )
        result = self.api.request(self.URL, 'GET')
        data = result.get('response')
        self.assertEqual(data, {'some': 'content'})

    def test_api_debug(self):
        """Validate the API with debug parameter set to True."""
        content = u'{"debug": true}'
        api_debug = self._callFUT(self.BASE_URL, debug=True)
        responses.add(
            responses.GET,
            self.URL,
            body=content,
            status=200,
        )
        result = api_debug.request(self.URL, 'GET')
        data = result.get('response')
        self.assertEqual(data, {'debug': True})

    def test_enveloped_headers(self):
        """Validate the headers returned from the API when they are enveloped
        with the API response.
        """
        content = u'{' + \
            u'"status": 200,' + \
            u'"headers":{"h1": "v1", "h2": "v2"},' + \
            u'"response": {"some": "content"}}'
        responses.add(
            responses.GET,
            self.URL,
            body=content,
            status=200,
        )
        result = self.api.request(self.URL, 'GET')
        headers = result.get('headers')
        self.assertEqual(headers, {'h1': 'v1', 'h2': 'v2'})

    def test_non_enveloped_headers(self):
        """Validate the headers returned from the API when they are not
        enveloped and only included as HTTP headers.
        """
        content = u'{"some": "content"}'
        headers = {
            'X-MLS-h1': 'v1',
            'X-MLS-h2': 'v2',
            'OtherHeader': 'v3',
        }
        responses.add(
            responses.GET,
            self.URL,
            body=content,
            adding_headers=headers,
            status=200,
        )
        result = self.api.request(self.URL, 'GET')
        response_headers = result.get('headers')
        self.assertEqual(response_headers, {'h1': 'v1', 'h2': 'v2'})
