import unittest

from wsgi_wovn import Store


class TestStore(unittest.TestCase):

    def test_init(self):
        self.assertTrue(Store())

    def test_settings_no_parameters(self):
        s = Store()
        self.assertEqual('path', s.settings().get('url_pattern'))
        self.assertEqual('/(?P<lang>[^/.?]+)',
                         s.settings().get('url_pattern_reg'))

    def test_settings_url_pattern_path(self):
        s = Store()
        s.settings({'url_pattern': 'path'})
        self.assertEqual('path', s.settings().get('url_pattern'))
        self.assertEqual('/(?P<lang>[^/.?]+)',
                         s.settings().get('url_pattern_reg'))

    def test_settings_url_pattern_subdomain(self):
        s = Store()
        s.settings({'url_pattern': 'subdomain'})
        self.assertEqual('subdomain', s.settings().get('url_pattern'))
        self.assertEqual('^(?P<lang>[^.]+)\.',
                         s.settings().get('url_pattern_reg'))

    def test_settings_url_pattern_query(self):
        s = Store()
        s.settings({'url_pattern': 'query'})
        self.assertEqual('query', s.settings().get('url_pattern'))
        self.assertEqual('((\\?.*&)|\\?)wovn=(?P<lang>[^&]+)(&|$)',
                         s.settings().get('url_pattern_reg'))
