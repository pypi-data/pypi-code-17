
import unittest

from webtest import TestApp



class BrowserTestCase(unittest.TestCase):

    layer = None

    def setUp(self):
        super(BrowserTestCase, self).setUp()
        self._testapp = TestApp(self.layer.make_wsgi_app())

    def publish(self, path, basic=None, headers=None, handle_errors=False):
        assert basic
        self._testapp.authorization = ('Basic', tuple(basic.split(':')))
        env = {'wsgi.handleErrors': handle_errors}
        response = self._testapp.get(path, extra_environ=env, headers=headers,
                                     expect_errors=handle_errors)
        return response
