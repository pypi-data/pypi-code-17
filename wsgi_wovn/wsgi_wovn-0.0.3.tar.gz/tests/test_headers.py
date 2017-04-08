import unittest

from urllib.parse import urlparse

from wsgi_wovn import Headers
from wsgi_wovn import Lang


class TestHeaders(unittest.TestCase):
    __chinese_languages = ('zh-CHS', 'zh-CHT')

    def test_init(self):
        h = Headers(self.__get_env(), self.__get_settings())
        self.assertTrue(h)

    ###

    def __test_init(self, env, settings, expected):
        h = Headers(
            self.__get_env(env),
            self.__get_settings(settings)
        )
        self.assertEqual(expected, h.url)

    def test_init_with_sample_url(self):
        self.__test_init(
            dict(url='https://wovn.io'),
            dict(),
            'wovn.io/'
        )

    def test_init_with_query_language(self):
        self.__test_init(
            dict(url='https://wovn.io/?wovn=en'),
            dict(url_pattern='query'),
            'wovn.io/?'
        )

    def test_init_with_query_language_without_slash(self):
        self.__test_init(
            dict(url='https://wovn.io?wovn=en'),
            dict(url_pattern='query'),
            'wovn.io/?'
        )

    def test_init_with_path_language(self):
        self.__test_init(
            dict(url='https://wovn.io/en'),
            dict(),
            'wovn.io/'
        )

    def test_init_with_domain_language(self):
        self.__test_init(
            dict(url='https://en.wovn.io/'),
            dict(url_pattern='subdomain'),
            'wovn.io/'
        )

    def test_init_with_path_language_with_query(self):
        self.__test_init(
            dict(url='https://wovn.io/en/?wovn=zh-CHS'),
            dict(),
            'wovn.io/?wovn=zh-CHS'
        )

    def test_init_with_domain_language_with_query(self):
        self.__test_init(
            dict(url='https://en.wovn.io/?wovn=zh-CHS'),
            dict(url_pattern='subdomain'),
            'wovn.io/?wovn=zh-CHS'
        )

    def test_init_with_path_language_with_query_without_slash(self):
        self.__test_init(
            dict(url='https://wovn.io/en?wovn=zh-CHS'),
            dict(),
            'wovn.io/?wovn=zh-CHS'
        )

    def test_init_with_domain_language_with_query_without_slash(self):
        self.__test_init(
            dict(url='https://en.wovn.io?wovn=zh-CHS'),
            dict(url_pattern='subdomain'),
            'wovn.io/?wovn=zh-CHS'
        )

    ###

    def __test_path_lang_subdomain(self, subdomain, path_lang, url=''):
        if len(url) == 0:
            url = 'https://%s.wovn.io'
        h = Headers(
            self.__get_env({'url': url % subdomain}),
            self.__get_settings({
                'url_pattern': 'subdomain',
                'url_pattern_reg': '^(?P<lang>[^.]+)\.'
            })
        )
        self.assertEqual(path_lang, h.path_lang())

    def test_path_lang_subdomain_empty(self):
        self.__test_path_lang_subdomain('', '')

    def test_path_lang_subdomain(self):
        for key in Lang.LANG.keys():
            self.__test_path_lang_subdomain(key, key)

    def test_path_lang_subdomain_uppercase(self):
        for key in Lang.LANG.keys():
            self.__test_path_lang_subdomain(key.upper(), key)

    def test_path_lang_subodmain_lowercase(self):
        for key in self.__chinese_languages:
            self.__test_path_lang_subdomain(key.lower(), key)

    ###

    def __test_path_lang_subdomain_with_slash(self, subdomain, path_lang):
        url = 'https://%s.wovn.io/'
        self.__test_path_lang_subdomain(subdomain, path_lang, url)

    def test_path_lang_subodmain_empty_with_slash(self):
        self.__test_path_lang_subdomain_with_slash('', '')

    def test_path_lang_subdomain_with_slash(self):
        for key in Lang.LANG.keys():
            self.__test_path_lang_subdomain_with_slash(key, key)

    def test_path_lang_subdomain_uppercase_with_slash(self):
        for key in Lang.LANG.keys():
            self.__test_path_lang_subdomain_with_slash(key.upper(), key)

    def test_path_lang_subdomain_lowercase_with_slash(self):
        for key in self.__chinese_languages:
            self.__test_path_lang_subdomain_with_slash(key.lower(), key)

    ###

    def __test_path_lang_subdomain_with_port(self, subdomain, path_lang):
        url = 'https://%s.wovn.io:1234'
        self.__test_path_lang_subdomain(subdomain, path_lang, url)

    def test_path_lang_subdomain_empty_with_port(self):
        self.__test_path_lang_subdomain_with_port('', '')

    def test_path_lang_subdomain_with_port(self):
        for key in Lang.LANG.keys():
            self.__test_path_lang_subdomain_with_port(key, key)

    def test_path_lang_subdomain_uppercase_with_port(self):
        for key in Lang.LANG.keys():
            self.__test_path_lang_subdomain_with_port(key.upper(), key)

    def test_path_lang_subdomain_lowercase_with_port(self):
        for key in self.__chinese_languages:
            self.__test_path_lang_subdomain_with_port(key.lower(), key)

    ###

    def __test_path_lang_subdomain_with_slash_with_port(
            self, subdomain, path_lang):
        url = 'https://%s.wovn.io:1234/'
        self.__test_path_lang_subdomain(subdomain, path_lang, url)

    def test_path_lang_subdomain_empty_with_slash_with_port(self):
        self.__test_path_lang_subdomain_with_slash_with_port('', '')

    def test_path_lang_subdomain_with_slash_with_port(self):
        for key in Lang.LANG.keys():
            self.__test_path_lang_subdomain_with_slash_with_port(key, key)

    def test_path_lang_subdomain_uppercase_with_slash_with_port(self):
        for key in Lang.LANG.keys():
            self.__test_path_lang_subdomain_with_slash_with_port(
                key.upper(), key)

    def test_path_lang_subdomain_lowercase_with_slash_with_port(self):
        for key in self.__chinese_languages:
            self.__test_path_lang_subdomain_with_slash_with_port(
                key.lower(), key)

    ###

    def __test_path_lang_subdomain_unsecure(self, subdomain, path_lang):
        url = 'http://%s.wovn.io'
        self.__test_path_lang_subdomain(subdomain, path_lang, url)

    def test_path_lang_subdomain_empty_unsecure(self):
        self.__test_path_lang_subdomain_unsecure('', '')

    def test_path_lang_subdomain_unsecure(self):
        for key in Lang.LANG.keys():
            self.__test_path_lang_subdomain_unsecure(key, key)

    def test_path_lang_subdomain_uppercase_unsecure(self):
        for key in Lang.LANG.keys():
            self.__test_path_lang_subdomain_unsecure(key.upper(), key)

    def test_path_lang_subdomain_lowercase_unsecure(self):
        for key in self.__chinese_languages:
            self.__test_path_lang_subdomain_unsecure(key.lower(), key)

    ###

    def __test_path_lang_subdomain_with_slash_unsecure(
            self, subdomain, path_lang):
        url = 'http://%s.wovn.io/'
        self.__test_path_lang_subdomain(subdomain, path_lang, url)

    def test_path_lang_subdomain_empty_with_slash_unsecure(self):
        self.__test_path_lang_subdomain_with_slash_unsecure('', '')

    def test_path_lang_subdomain_with_slash_unsecure(self):
        for key in Lang.LANG.keys():
            self.__test_path_lang_subdomain_with_slash_unsecure(key, key)

    def test_path_lang_subdomain_uppercase_with_slash_unsecure(self):
        for key in Lang.LANG.keys():
            self.__test_path_lang_subdomain_with_slash_unsecure(
                key.upper(), key)

    def test_path_lang_subdomain_lowercase_with_slash_unsecure(self):
        for key in self.__chinese_languages:
            self.__test_path_lang_subdomain_with_slash_unsecure(
                key.lower(), key)

    ###

    def __test_path_lang_subdomain_with_port_unsecure(
            self, subdomain, path_lang):
        url = 'http://%s.wovn.io:1234'
        self.__test_path_lang_subdomain(subdomain, path_lang, url)

    def test_path_lang_subdomain_empty_with_port_unsecure(self):
        self.__test_path_lang_subdomain_with_port_unsecure('', '')

    def test_path_lang_subdomain_with_port_unsecure(self):
        for key in Lang.LANG.keys():
            self.__test_path_lang_subdomain_with_port_unsecure(key, key)

    def test_path_lang_subdomain_uppercase_with_port_unsecure(self):
        for key in Lang.LANG.keys():
            self.__test_path_lang_subdomain_with_port_unsecure(
                key.upper(), key)

    def test_path_lang_subdomain_lowercase_with_port_unsecure(self):
        for key in self.__chinese_languages:
            self.__test_path_lang_subdomain_with_port_unsecure(
                key.lower(), key)

    ###

    def __test_path_lang_subdomain_with_slash_with_port_unsecure(
            self, subdomain, path_lang):
        url = 'http://%s.wovn.io:1234/'
        self.__test_path_lang_subdomain(subdomain, path_lang, url)

    def test_path_lang_subdomain_empty_with_slash_with_port_unsecure(self):
        self.__test_path_lang_subdomain_with_slash_with_port_unsecure('', '')

    def test_path_lang_subdomain_with_slash_with_port_unsecure(self):
        for key in Lang.LANG.keys():
            self.__test_path_lang_subdomain_with_slash_with_port_unsecure(
                key, key)

    def test_path_lang_subdomain_uppercase_with_slash_with_port_unsecure(self):
        for key in Lang.LANG.keys():
            self.__test_path_lang_subdomain_with_slash_with_port_unsecure(
                key.upper(), key)

    def test_path_lang_subdomain_lowercase_with_slash_with_port_unsecure(self):
        for key in self.__chinese_languages:
            self.__test_path_lang_subdomain_with_slash_with_port_unsecure(
                key.lower(), key)

    ###

    def __test_path_lang_query(self, query, path_lang, url=''):
        if len(url) == 0:
            url = 'https://wovn.io?wovn=%s'
        h = Headers(
            self.__get_env({'url': url % query}),
            self.__get_settings({
                'url_pattern': 'query',
                'url_pattern_reg': '((\?.*&)|\?)wovn=(?P<lang>[^&]+)(&|$)'
            })
        )
        self.assertEqual(path_lang, h.path_lang())

    def test_path_lang_query_empty(self):
        self.__test_path_lang_query('', '')

    def test_path_lang_query(self):
        for key in Lang.LANG.keys():
            self.__test_path_lang_query(key, key)

    def test_path_lang_query_uppercase(self):
        for key in Lang.LANG.keys():
            self.__test_path_lang_query(key.upper(), key)

    def test_path_lang_query_lowercase(self):
        for key in self.__chinese_languages:
            self.__test_path_lang_query(key.lower(), key)

    ###

    def __test_path_lang_query_with_slash(self, query, path_lang):
        url = 'https://wovn.io/?wovn=%s'
        self.__test_path_lang_query(query, path_lang, url)

    def test_path_lang_query_empty_with_slash(self):
        self.__test_path_lang_query_with_slash('', '')

    def test_path_lang_query_with_slash(self):
        for key in Lang.LANG.keys():
            self.__test_path_lang_query_with_slash(key, key)

    def test_path_lang_query_uppercase_with_slash(self):
        for key in Lang.LANG.keys():
            self.__test_path_lang_query_with_slash(key.upper(), key)

    def test_path_lang_query_lowercase_with_slash(self):
        for key in self.__chinese_languages:
            self.__test_path_lang_query_with_slash(key.lower(), key)

    ###

    def __test_path_lang_query_with_port(self, query, path_lang):
        url = 'https://wovn.io:1234?wovn=%s'
        self.__test_path_lang_query(query, path_lang, url)

    def test_path_lang_query_empty_with_port(self):
        self.__test_path_lang_query_with_port('', '')

    def test_path_lang_query_with_port(self):
        for key in Lang.LANG.keys():
            self.__test_path_lang_query_with_port(key, key)

    def test_path_lang_query_uppercase_with_port(self):
        for key in Lang.LANG.keys():
            self.__test_path_lang_query_with_port(key.upper(), key)

    def test_path_lang_query_lowercase_with_port(self):
        for key in self.__chinese_languages:
            self.__test_path_lang_query_with_port(key.lower(), key)

    ###

    def __test_path_lang_query_with_slash_with_port(self, query, path_lang):
        url = 'https://wovn.io:1234/?wovn=%s'
        self.__test_path_lang_query(query, path_lang, url)

    def test_path_lang_query_empty_with_slash_with_port(self):
        self.__test_path_lang_query_with_slash_with_port('', '')

    def test_path_lang_query_with_slash_with_port(self):
        for key in Lang.LANG.keys():
            self.__test_path_lang_query_with_slash_with_port(key, key)

    def test_path_lang_query_uppercase_with_slash_with_port(self):
        for key in Lang.LANG.keys():
            self.__test_path_lang_query_with_slash_with_port(key.upper(), key)

    def test_path_lang_query_lowercase_with_slash_with_port(self):
        for key in self.__chinese_languages:
            self.__test_path_lang_query_with_slash_with_port(key.lower(), key)

    ###

    def __test_path_lang_query_unsecure(self, query, path_lang):
        url = 'http://wovn.io?wovn=%s'
        self.__test_path_lang_query(query, path_lang, url)

    def test_path_lang_query_empty_unsecure(self):
        self.__test_path_lang_query_unsecure('', '')

    def test_path_lang_query_unsecure(self):
        for key in Lang.LANG.keys():
            self.__test_path_lang_query_unsecure(key, key)

    def test_path_lang_query_uppercase_unsecure(self):
        for key in Lang.LANG.keys():
            self.__test_path_lang_query_unsecure(key.upper(), key)

    def test_path_lang_query_lowercase_unsecure(self):
        for key in self.__chinese_languages:
            self.__test_path_lang_query_unsecure(key.lower(), key)

    ###

    def __test_path_lang_query_with_slash_unsecure(self, query, path_lang):
        url = 'http://wovn.io/?wovn=%s'
        self.__test_path_lang_query(query, path_lang, url)

    def test_path_lang_query_empty_with_slash_unsecure(self):
        self.__test_path_lang_query_with_slash_unsecure('', '')

    def test_path_lang_query_with_slash_unsecure(self):
        for key in Lang.LANG.keys():
            self.__test_path_lang_query_with_slash_unsecure(key, key)

    def test_path_lang_query_uppercase_with_slash_unsecure(self):
        for key in Lang.LANG.keys():
            self.__test_path_lang_query_with_slash_unsecure(key.upper(), key)

    def test_path_lang_query_lowercase_with_slash_unsecure(self):
        for key in self.__chinese_languages:
            self.__test_path_lang_query_with_slash_unsecure(key.lower(), key)

    ###

    def __test_path_lang_query_with_port_unsecure(self, query, path_lang):
        url = 'http://wovn.io:1234?wovn=%s'
        self.__test_path_lang_query(query, path_lang, url)

    def test_path_lang_query_empty_with_port_unsecure(self):
        self.__test_path_lang_query_with_port_unsecure('', '')

    def test_path_lang_query_with_port_unsecure(self):
        for key in Lang.LANG.keys():
            self.__test_path_lang_query_with_port_unsecure(key, key)

    def test_path_lang_query_uppercase_with_port_unsecure(self):
        for key in Lang.LANG.keys():
            self.__test_path_lang_query_with_port_unsecure(key.upper(), key)

    def test_path_lang_query_lowercase_with_port_unsecure(self):
        for key in self.__chinese_languages:
            self.__test_path_lang_query_with_port_unsecure(key.lower(), key)

    ###

    def __test_path_lang_query_with_slash_with_port_unsecure(
            self, query, path_lang):
        url = 'http://wovn.io:1234/?wovn=%s'
        self.__test_path_lang_query(query, path_lang, url)

    def test_path_lang_query_empty_with_slash_with_port_unsecure(self):
        self.__test_path_lang_query_with_slash_with_port_unsecure('', '')

    def test_path_lang_query_with_slash_with_port_unsecure(self):
        for key in Lang.LANG.keys():
            self.__test_path_lang_query_with_slash_with_port_unsecure(key, key)

    def test_path_lang_query_uppercase_with_slash_with_port_unsecure(self):
        for key in Lang.LANG.keys():
            self.__test_path_lang_query_with_slash_with_port_unsecure(
                key.upper(), key)

    def test_path_lang_query_lowercase_with_slash_with_port_unsecure(self):
        for key in self.__chinese_languages:
            self.__test_path_lang_query_with_slash_with_port_unsecure(
                key.lower(), key)

    ###

    def __test_path_lang_path(self, path, path_lang, url=''):
        if len(url) == 0:
            url = 'https://wovn.io/%s'
        h = Headers(
            self.__get_env({'url': url % path}),
            self.__get_settings()
        )
        self.assertEqual(path_lang, h.path_lang())

    def test_path_lang_path_empty(self):
        url = 'https://wovn.io%s'
        self.__test_path_lang_path('', '', url)

    def test_path_lang_path_empty_with_slash(self):
        self.__test_path_lang_path('', '')

    def test_path_lang_path_with_slash(self):
        for key in Lang.LANG.keys():
            self.__test_path_lang_path(key, key)

    def test_path_lang_path_uppercase_with_slash(self):
        for key in Lang.LANG.keys():
            self.__test_path_lang_path(key.upper(), key)

    def test_path_lang_path_lowercase_with_slash(self):
        for key in self.__chinese_languages:
            self.__test_path_lang_path(key.lower(), key)

    ###

    def __test_path_lang_path_with_port(self, path, path_lang):
        url = 'https://wovn.io:1234/%s'
        self.__test_path_lang_path(path, path_lang, url)

    def test_path_lang_path_empty_with_port(self):
        url = 'https://wovn.io:1234%s'
        self.__test_path_lang_path('', '', url)

    def test_path_lang_path_empty_with_slash_with_port(self):
        self.__test_path_lang_path_with_port('', '')

    def test_path_lang_path_with_port(self):
        for key in Lang.LANG.keys():
            self.__test_path_lang_path_with_port(key, key)

    def test_path_lang_path_uppercase_with_port(self):
        for key in Lang.LANG.keys():
            self.__test_path_lang_path_with_port(key.upper(), key)

    def test_path_lang_path_lowercase_with_port(self):
        for key in self.__chinese_languages:
            self.__test_path_lang_path_with_port(key.lower(), key)

    ###

    def __test_path_lang_path_unsecure(self, path, path_lang):
        url = 'http://wovn.io/%s'
        self.__test_path_lang_path(path, path_lang, url)

    def test_path_lang_path_empty_unsecure(self):
        url = 'http://wovn.io%s'
        self.__test_path_lang_path('', '', url)

    def test_path_lang_path_empty_with_slash_unsecure(self):
        self.__test_path_lang_path_unsecure('', '')

    def test_path_lang_path_unsecure(self):
        for key in Lang.LANG.keys():
            self.__test_path_lang_path_unsecure(key, key)

    def test_path_lang_path_uppercase_unsecure(self):
        for key in Lang.LANG.keys():
            self.__test_path_lang_path_unsecure(key.upper(), key)

    def test_path_lang_path_lowercase_unsecure(self):
        for key in self.__chinese_languages:
            self.__test_path_lang_path_unsecure(key.lower(), key)

    ###

    def __test_path_lang_path_with_port_unsecure(self, path, path_lang):
        url = 'http://wovn.io:1234/%s'
        self.__test_path_lang_path(path, path_lang, url)

    def test_path_lang_path_empty_with_port__unsecure(self):
        url = 'http://wovn.io:1234%s'
        self.__test_path_lang_path('', '', url)

    def test_path_lang_path_empty_with_slash_with_port_unsecure(self):
        self.__test_path_lang_path_with_port_unsecure('', '')

    def test_path_lang_path_with_port_unsecure(self):
        for key in Lang.LANG.keys():
            self.__test_path_lang_path_with_port_unsecure(key, key)

    def test_path_lang_path_uppercase_with_port_unsecure(self):
        for key in Lang.LANG.keys():
            self.__test_path_lang_path_with_port_unsecure(key.upper(), key)

    def test_path_lang_path_lowercase_with_port_unsecure(self):
        for key in self.__chinese_languages:
            self.__test_path_lang_path_with_port_unsecure(key.lower(), key)

    ###

    def __get_env(self, options={}):
        env = {}
        env['rack.url_scheme'] = 'http'
        env['HTTP_HOST'] = 'wovn.io'
        env['SERVER_NAME'] = 'wovn.io'
        env['HTTP_ACCEPT_LANGUAGE'] = 'ja,en-US;q=0.8,en;q=0.6'
        env['QUERY_STRING'] = 'param=val&hey=you'
        env['PATH_INFO'] = '/dashboard'

        if options.get('url'):
            url = urlparse(options['url'])
            env['wsgi.url_scheme'] = url.scheme
            env['HTTP_HOST'] = url.netloc
            env['SERVER_NAME'] = url.netloc
            env['QUERY_STRING'] = url.query
            env['PATH_INFO'] = url.path or '/'

        dicts = [env, options]
        return {k: v for dic in dicts for k, v in dic.items()}

    def __get_settings(self, options={}):
        settings = {}
        settings['user_token'] = 'OHYx9'
        settings['url_pattern'] = 'path'
        settings['url_pattern_reg'] = r'/(?P<lang>[^/.?]+)'
        settings['query'] = []
        settings['api_url'] = 'http://localhost/v0/values'
        settings['default_lang'] = 'en'
        settings['supported_langs'] = []
        settings['secret_key'] = ''

        dicts = [settings, options]
        return {k: v for dic in dicts for k, v in dic.items()}
