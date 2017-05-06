# coding: utf-8

import os
import time
import uuid
import random
from hashlib import sha1

char_alphabet = "abcdefghijklmnopqrstuvwxyz"
char_digit = "0123456789"

def random_ascii(length, digit=True, ignorecase=False, drops=None ):

    global char_alphabet, char_digit

    chars = char_alphabet
    if digit:
        chars += char_digit
    if not ignorecase:
        chars += char_alphabet.upper()

    if isinstance(drops, str):
        L = list(chars)
        for drop in drops:
            if drop in L:
                L.remove(drop)
        chars = ''.join(L)

    if length < len(chars):
        return ''.join(random.sample(chars, length))
    else:
        r_list = []
        for i in range(length):
            r_list.append(random.choice(chars))

        return ''.join(r_list)


def random_digit(length):

    global char_digit

    chars = char_digit

    if length < len(chars):
        return ''.join(random.sample(chars, length))
    else:
        r_list = []
        for i in range(length):
            r_list.append(random.choice(chars))

        return ''.join(r_list)


def random_sha1():
    s = sha1( os.urandom(256) )
    s.update( str(time.time()) )
    s.update( str(random.randrange(1, 100000000)) )
    key = s.hexdigest()
    return key


def gen_uuid():
    return  str(uuid.uuid4())


# 参考： salt/utils/__init__.py
def gen_mac(prefix='AC:DE:48'):
    '''
    Generates a MAC address with the defined OUI prefix.

    Common prefixes:

     - ``00:16:3E`` -- Xen
     - ``00:18:51`` -- OpenVZ
     - ``00:50:56`` -- VMware (manually generated)
     - ``52:54:00`` -- QEMU/KVM
     - ``AC:DE:48`` -- PRIVATE

    References:

     - http://standards.ieee.org/develop/regauth/oui/oui.txt
     - https://www.wireshark.org/tools/oui-lookup.html
     - https://en.wikipedia.org/wiki/MAC_address
    '''
    return '{0}:{1:02X}:{2:02X}:{3:02X}'.format(
        prefix,
        random.randint(0, 0xff),
        random.randint(0, 0xff),
        random.randint(0, 0xff) )



if __name__ == '__main__':

    print('random_sha1()    : %s' % random_sha1())
    print('random_ascii(40) : %s' % random_ascii(40))

