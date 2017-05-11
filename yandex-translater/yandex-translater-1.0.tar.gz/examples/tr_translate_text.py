#-*- coding: utf-8 -*-

from yandex.Translate import Translate

tr = Translate()

key = 'yandex_key' 

tr.set_key(key)

tr.set_text('Hello Yandex')

tr.set_from_lang('en')

tr.set_to_lang('ru')


print(tr.translate())

