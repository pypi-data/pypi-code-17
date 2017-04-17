# -*- coding: utf-8 -*-

import cStringIO
import sys

def StdoutToBuffer(function, *args, **kwargs):
    buff = cStringIO.StringIO()
    stdout = sys.stdout
    sys.stdout = buff
    try:
        function(*args, **kwargs)
    finally:
        sys.stdout = stdout
    return buff.getvalue()
