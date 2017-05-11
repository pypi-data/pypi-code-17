#-*- coding: utf-8 -*-

from yandex import Translater
import unittest

class TestYandexTranslater(unittest.TestCase):

    def test_ins(self):
        tr = Translater()
        self.assertEqual(type(tr), Translater)
        print('test_ins -> Ok.')

    def test_empty_api_key(self):
        tr = Translater()
        self.assertEqual(type(tr), Translater)
        tr.set_key('')
        result = tr.translate()
        self.assertEqual(type(result), str)
        self.assertEqual(result, 'Please set Api key')
        print('test_empty_api_key -> Ok.')

    def test_empty_text(self):
        tr = Translater()
        self.assertEqual(type(tr), Translater)
        tr.set_key('IaMiNvAlIdKeY')
        result = tr.translate()
        self.assertEqual(type(result), str) 
        self.assertEqual(result, 'Please set Text')
        print('test_empty_text -> Ok.')

    def test_empty_from_lang(self):
        tr = Translater()
        self.assertEqual(type(tr), Translater)
        tr.set_key('IaMiNvAlIdKeY')
        tr.set_text('Hello Yandex')
        result = tr.translate()
        self.assertEqual(type(result), str)
        self.assertEqual(result, 'Please set source lang')
        print('test_empty_from_lang -> Ok.')

    def test_empty_to_lang(self):
        tr = Translater()
        self.assertEqual(type(tr), Translater)
        tr.set_key('IaMiNvAlIdKeY')
        tr.set_text('Hello Yandex')
        tr.set_from_lang('en')
        result = tr.translate()
        self.assertEqual(type(result), str)
        self.assertEqual(result, 'Please set destination lang')
        print('test_empty_to_lang -> Ok.')

    def test_forbiden_api_key(self):
        tr = Translater()
        self.assertEqual(type(tr), Translater)
        tr.set_key('IaMiNvAlIdKeY')
        tr.set_text('Hello Yandex')
        tr.set_from_lang('en')
        tr.set_to_lang('ru')
        result = tr.translate()
        self.assertEqual(type(result), str)
        self.assertEqual(result, 'Failed to translate text! Forbidden')
        print('test_forbiden_api_key -> Ok.')

    def test_blocked_api_key(self):
        tr = Translater()
        self.assertEqual(type(tr), Translater)
        tr.set_key('trnsl.1.1.20170425T124714Z.2bfd03d640900137.1a0c8f628383717958530d14d22bd35814ea2545')
        tr.set_text('Hello Yandex')
        tr.set_from_lang('en')
        tr.set_to_lang('ru')
        result = tr.translate()
        self.assertEqual(type(result), str)
        self.assertEqual(result, 'Failed to translate text! Forbidden')
        print('test_blocked_api_key -> Ok.')

    def test_valid_api_key(self):    
        tr = Translater()
        self.assertEqual(type(tr), Translater)
        tr.set_key('trnsl.1.1.20170502T185327Z.003373b7b88cddda.5420c79cd704be7b9538b3e7d9ea9e7db457a4e7')
        tr.set_text('Hello Yandex')
        tr.set_from_lang('en')
        tr.set_to_lang('ru')
        result = tr.translate()
        self.assertEqual(type(result), str)
        self.assertEqual(result, 'Здравствуйте Яндекса')
        print('test_valid_api_key -> Ok.')

    def test_get_langs(self):
        tr = Translater()
        self.assertEqual(type(tr), Translater)
        tr.set_key('trnsl.1.1.20170502T185327Z.003373b7b88cddda.5420c79cd704be7b9538b3e7d9ea9e7db457a4e7')
        result = tr.get_langs()
        self.assertEqual(type(result), list)
        print('test_get_langs -> Ok.')

    def test_detect_lang(self):
        tr = Translater()
        self.assertEqual(type(tr), Translater)
        tr.set_key('trnsl.1.1.20170502T185327Z.003373b7b88cddda.5420c79cd704be7b9538b3e7d9ea9e7db457a4e7')
        tr.set_hint('en','ru','ar')
        tr.set_text('Привет Мир')
        result = tr.detect_lang()
        self.assertEqual(type(result), str)
        self.assertEqual(result, 'ru')
        print('test_detect_lang -> Ok.')

if __name__ == '__main__':
        unittest.main()

