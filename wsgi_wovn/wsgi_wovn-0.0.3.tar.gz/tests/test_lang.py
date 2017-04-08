import unittest

from wsgi_wovn import Lang


class TestLang(unittest.TestCase):

    def test_langs_exist(self):
        self.assertTrue(Lang.LANG)

    def test_keys_exist(self):
        for k, v in Lang.LANG.items():
            self.assertTrue('name' in v)
            self.assertTrue('code' in v)
            self.assertTrue('en' in v)
            self.assertEqual(k, v['code'])

    def test_get_code_with_valid_code(self):
        self.assertEqual('ms', Lang.get_code('ms'))

    def test_get_code_with_capital_letters(self):
        self.assertEqual('zh-CHT', Lang.get_code('zh-cht'))

    def test_get_code_with_valid_english_name(self):
        self.assertEqual('pt', Lang.get_code('Portuguese'))

    def test_get_code_with_valid_native_name(self):
        self.assertEqual('hi', Lang.get_code('हिन्दी'))

    def test_get_code_with_invalid_name(self):
        self.assertIsNone(Lang.get_code('WOVN4LYFE'))

    def test_get_code_with_empty_string(self):
        self.assertIsNone(Lang.get_code(''))

    def test_get_code_with_nil(self):
        self.assertIsNone(Lang.get_code(None))
