# coding: utf-8
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import print_function
from future.utils import python_2_unicode_compatible

import base64

from django.conf import settings
from Crypto.Cipher import AES


_cipher = None


@python_2_unicode_compatible
class AESCipher(object):
    '''
    from http://qiita.com/teitei_tk/items/0b8bae99a8700452b718
    $ python -c "import string, random; print(''.join(
       [random.choice(string.ascii_letters + string.digits) for i in range(50)]))"
    '''
    def __init__(self, key, block_size=32):
        self.bs = block_size
        if len(key) >= block_size:
            self.key = key[:block_size]
        else:
            self.key = self._pad(key)

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = settings.CRYPTO_KEY[:AES.block_size]
        if len(iv) < AES.block_size:
            iv += b'x' * (AES.block_size - len(iv))
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:]))

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    def _unpad(self, s):
        return s[:-ord(s[len(s) - 1:])]


def __get_cipher():

    global _cipher
    if _cipher is None:
        _cipher = AESCipher(settings.CRYPTO_KEY)
    return _cipher


def aes_encrypt(value):
    return __get_cipher().encrypt(value)


def aes_decrypt(value):
    return __get_cipher().decrypt(value)
