import hashlib
import inspect
import os
import re

from time import time


RE_COMMENTS = re.compile("#(.*)$", re.MULTILINE)


def bgcache_home():
    return os.getenv('BGCACHE_HOME', os.path.expanduser("~/.bgcache"))


def md5_code(code):
    source = inspect.getsource(code)
    source_clean = RE_COMMENTS.sub("", source.replace(' ', '').replace('\t', '')).replace('\n', '')
    return hashlib.md5(source_clean.encode('utf-8')).hexdigest()


def md5_file(fname):
    t_ini = time()
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(1048576), b""):
            hash_md5.update(chunk)

    return hash_md5.hexdigest(), time() - t_ini