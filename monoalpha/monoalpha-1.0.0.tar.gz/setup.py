from setuptools import *
setup(
name="monoalpha",
version="1.0.0",
description="A simple monoalphabetic cipher program.",
long_description="""Monoalpha can be used to generate generate code
alphabets, as well as encrypting, and decrypting
text. It supports caesar shift, ROT13, affine, atbash,
and keyword ciphers. It can also encrypt and decrypt
based on your own code alphabets.""",
author="Toby Govin-Fowler",
author_email="ttoobbyyninja@gmail.com",
license="MIT",
classifiers=["Development Status :: 5 - Production/Stable",

               "Intended Audience :: Developers",
               "Topic :: Security :: Cryptography",

               "License :: OSI Approved :: MIT License",

               "Programming Language :: Python",
               "Programming Language :: Python :: 2",
               "Programming Language :: Python :: 3",
],
keywords="cipher monoalphabetic encrypt",
packages=find_packages(),
entry_points={
    "console_scripts":[
        "monoalpha=monoalpha.commandline:runcmd"
        ]
    }
)
