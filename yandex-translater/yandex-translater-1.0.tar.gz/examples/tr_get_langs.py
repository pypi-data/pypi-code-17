#-*- coding: utf-8 -*-

from yandex.Translate import Translate

tr = Translate()

key = 'yandex_key'

tr.set_key(key)

print(' '.join(tr.get_langs()))

