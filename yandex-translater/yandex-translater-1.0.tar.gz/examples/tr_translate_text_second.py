#-*- coding: utf-8 -*-

from yandex.Translate import Translate

key = 'yandex_key' 

tr = Translate(key=key, text='Hello yandex', from_lang = 'en',
              to_lang = 'ru')

print (tr.translate())

