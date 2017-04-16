"""
MIT License

Copyright (c) 2017 Kim Blomqvist

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from os import path
from os import chmod
import pytoml as toml

CALLBACK_URI = ('localhost', 1337)
WITHINGS_API_URI = 'https://wbsapi.withings.net'
WITHINGS_OAUTH_URI = 'https://oauth.withings.com/account'
CONFIG_FILE = path.join(path.expanduser("~"), '.withings')

try:
    with open(CONFIG_FILE, 'r') as file:
        CONFIG = toml.load(file)
except EnvironmentError:
    CONFIG = dict()
    CONFIG['users'] = dict()

def save_confile():
    with open(CONFIG_FILE, 'w') as file:
        toml.dump(CONFIG, file)
    chmod(CONFIG_FILE, 0o600)

import atexit
atexit.register(save_confile)
