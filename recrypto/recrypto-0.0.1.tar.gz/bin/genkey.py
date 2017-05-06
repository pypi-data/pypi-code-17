#!/usr/bin/env python
# -*- coding: utf-8 -*-

from recrypto import genprivkey, genpubkey

if __name__ == '__main__':
    import sys
    if len(sys.argv) == 2:
        # genkey.py <seed>
        priv, pub = genprivkey(sys.argv[1].encode())
        print('private key:', priv.decode())
        print('public key:', pub.decode())
    elif len(sys.argv) == 3:
        # genkey.py <privkey> <pubkey>
        pub = genpubkey(sys.argv[2].encode())
        print('yes' if pub == sys.argv[1].encode() else 'no')
