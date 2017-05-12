# encoding: utf-8

u"""
====================================================
Used to return a response that has already been made
and pickled. This includes headers, status etc.

Modifiers that change the URI have no effect.

Modifiers that change the response will still be
applied

To get the pickled string, use Python:

>>> import requests
>>> import pickle
>>> r = requests.get(u'http://www.google.com')
>>> print(pickle.dumps(r))

----------------------------------------------------
Filter     : String to match in the request URI
Override   : N/A
Parameters : string containing a pickled requests
             object representing the canned response
====================================================
"""

import pickle


def modify(uri,
           parameters):

    if parameters.filter in uri:
        return pickle.loads(parameters.params.decode(u'unicode_escape'))

    return None
