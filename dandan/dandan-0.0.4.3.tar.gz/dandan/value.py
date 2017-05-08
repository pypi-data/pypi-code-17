#!/usr/bin/python2
# encoding=utf-8
import json


class AttrDict(dict):
    def __init__(self, dic={}, json_string=None, *args, **kwargs):
        for arg in args:
            for var in arg:
                self[var[0]] = var[1]
        for key in kwargs:
            self[key] = kwargs[key]
        for key in dic:
            self[key] = dic[key]
        if json_string:
            dic = json.loads(json_string)
        for key in dic:
            self[key] = dic[key]

    def __getattr__(self, key):
        if key not in self:
            self[key] = AttrDict()
        return self[key]

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        del self[key]

    def __delitem__(self, key):
        if key not in self:
            return
        dict.__delitem__(self, key)

    def __getitem__(self, key):
        if key not in self:
            self[key] = AttrDict()
        return dict.__getitem__(self, key)

    def __setitem__(self, key, value):
        if type(value) == dict:
            value = AttrDict(**value)
        dict.__setitem__(self, key, value)

    def dict(self):
        res = {}
        for var in self:
            value = self[var]
            if isinstance(value, AttrDict):
                value = value.dict()
            res[var] = value
        return res

    def __getstate__(self):
        return self.dict()

    def __setstate__(self, state):
        pass

    def __add__(self, other):
        if not self:
            return other
        raise Exception("Dict not empty.")

    def __sub__(self, other):
        if not self:
            return -other
        raise Exception("Dict not empty.")

    def __str__(self):
        return super(AttrDict, self).__str__()

    def __unicode__(self):
        return super(AttrDict, self).__str__()

# function


def get_pickle(filename):
    import os
    import cPickle as pickle
    if not os.path.exists(filename):
        return None
    try:
        with open(filename, "rb") as f:
            data = pickle.load(f)
            return data
    except Exception:
        return None


def put_pickle(data, filename):
    import os
    import cPickle as pickle
    filename = os.path.abspath(filename)
    dirname = os.path.dirname(filename)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    with open(filename, "wb") as f:
        pickle.dump(data, f)


def get_json(filename):
    import os
    import json
    if not os.path.exists(filename):
        return None
    try:
        with open(filename, "rb") as f:
            data = json.loads(f.read())
            return data
    except Exception:
        return None


def put_json(data, filename):
    import os
    import json
    filename = os.path.abspath(filename)
    dirname = os.path.dirname(filename)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    with open(filename, "wb") as f:
        f.write(json.dumps(data))


def md5(data=None, filename=None):
    import hashlib
    m = hashlib.md5()
    if data:
        m.update(data)
    if filename:
        with open(filename, "rb") as f:
            while True:
                block = f.read(16 * 1024)
                if not block:
                    break
                m.update(block)
    return m.hexdigest()


def sha1(data=None, filename=None):
    import hashlib
    m = hashlib.sha1()
    if data:
        m.update(data)
    if filename:
        with open(filename, "rb") as f:
            while True:
                block = f.read(16 * 1024)
                if not block:
                    break
                m.update(block)
    return m.hexdigest()


if __name__ == '__main__':
    data = AttrDict()

    print unicode(data)
