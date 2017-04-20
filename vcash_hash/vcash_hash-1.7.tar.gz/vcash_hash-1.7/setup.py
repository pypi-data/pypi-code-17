from distutils.core import setup, Extension

vcash_hash_module = Extension('vcash_hash',
                                 sources = ['vcashmodule.c',
                                            'vcashhash.c',
                                            'sha3/blake.c',
                                            'sha3/whirlpool.c'],
                                 include_dirs=['.', './sha3'])

setup (name = 'vcash_hash',
       version = '1.7',
       description = 'Binding for Vcash Proof-of-Work hashing (Whirlpoolx & Blake256 8rounds).',
       maintainer = 'xCoreDev',
       maintainer_email = 'xCore@vchain.info',
       url = 'https://github.com/xCoreDev/python-vcash_hash',
       download_url = 'https://github.com/xCoreDev/python-vcash_hash/tarball/1.7',
       keywords = ['vcash', 'whirlpoolx', 'blake'],
       ext_modules = [vcash_hash_module])
