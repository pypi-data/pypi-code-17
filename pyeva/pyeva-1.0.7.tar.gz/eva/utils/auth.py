# coding: UTF-8

import hashlib
import crypt
import time
import random
import logging
import base64
import pickle

from eva.utils.random_ import random_ascii


def _encrypt_password(salt, raw_password):
    data = "{0}{1}".format(salt, raw_password)
    hsh = hashlib.sha512(data.encode("UTF-8")).hexdigest()
    return hsh


def enc_login_passwd(plaintext):
    salt = random_ascii(128)
    hsh = _encrypt_password(salt, plaintext)
    enc_password = "%s$%s" % (salt, hsh)

    return enc_password


def check_login_passwd(raw_password, enc_password):
    try:
        salt, hsh = enc_password.split('$')
    except:
        return False
    return hsh == _encrypt_password(salt, raw_password)


def enc_shadow_passwd(plaintext):
    # get shadow passwd

    salt = crypt.crypt(str(random.random()), str(time.time()))[:8]
    s = '$'.join(['', '6', salt, ''])
    password = crypt.crypt(plaintext, s)

    return password


def encode_data(data, skey):
    pickle_data = pickle.dumps(data, pickle.HIGHEST_PROTOCOL)
    tamper_data = hashlib.md5(pickle_data + skey).hexdigest()
    return base64.encodestring(pickle_data + tamper_data)


def decode_data(data, skey):
    data = base64.decodestring(data)
    pickle_data, tamper_data = data[:-32], data[-32:]

    if hashlib.md5(pickle_data + skey).hexdigest() != tamper_data:
        logging.warning("User tampered with session cookie.")
        return None
    else:
        return pickle.loads(pickle_data)


if __name__ == '__main__':
    print("abc = ", enc_login_passwd('abc'))
    print("check 'abc' = ", check_login_passwd('abc',
                                               "Jnk98QdR2h1taHH1FXCepF3S9thooado8ihxxYlThRw8INymLYgpntexHgaTbL4uihdr5jdNMo2ah3o5gwgyEJGkq1yYcr2YCVlT7Td6z9AnzS5dC6lNv42iRCFPzYIR$4978038e77e1f6777a81bd64f0878a4283d75818306beb8e2e68413a3cdea413"))
    exit()

    skey = 'testfor'

    edata = encode_data({'user_id': 5}, skey)
    print('edata = {0}'.format(edata))

    #    skey = 'testfo'
    data = decode_data(edata, skey)
    print('data = {0}'.format(data))
