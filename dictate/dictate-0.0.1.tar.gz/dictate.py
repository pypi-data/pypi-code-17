#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hashlib import md5


__version__ = '0.0.1'


def _key_rule(k):
    if k.startswith('[') and k.endswith(']'):
        k = int(k[1:-1])
    return k


def retrieve_dict(doc, dot_key):
    """
    Could index value out by dot_key like this:
        foo.bar.[0].player

    """
    def recurse_dict(d, klist):
        try:
            k = klist.pop(0)
        except IndexError:
            return d

        d = d[_key_rule(k)]
        return recurse_dict(d, klist)

    sp_keys = dot_key.split('.')

    return recurse_dict(doc, sp_keys)


def map_dict(o):
    def recurse_doc(mapping, d, pk):
        if isinstance(d, dict):
            for k, v in d.iteritems():
                if pk is None:
                    ck = k
                else:
                    ck = pk + '.' + k
                recurse_doc(mapping, v, ck)
        elif isinstance(d, list):
            for loop, i in enumerate(d):
                ck = pk + '.' + '[%s]' % loop
                recurse_doc(mapping, i, ck)
        else:
            mapping[pk] = d
        return mapping

    return recurse_doc({}, o, None)


def hash_dict(o):
    """
    As dict is not hashable, this function is to generate a hash string
    from a dict unnormally, use every key & value of the dict,
    join then up and compute its md5 value.
    """
    seprator = '\n'
    mapping = map_dict(o)
    keys = mapping.keys()

    # get rid the random effect of dict keys, to ensure same dict will result to same value.
    keys.sort()

    string = seprator.join(['%s:%s' % (k, mapping[k]) for k in keys])
    return md5(string).hexdigest()


def diff_dicts(new, origin):
    """Only compare the first layer, return a the dict that represent
    add, remove, modify changes from new to origin

    NOTE: If one of the two dicts comes from another, eg. from .copy(),
    # make sure new and origin are totally different from each other,
    that means, the result may not be as you think. So use deepcopy in case.
    """
    diff = {
        '+': {},
        '-': [],
        '~': {}
    }
    for k, v in new.iteritems():
        if k not in origin:
            diff['+'][k] = v
            continue
        if v != origin[k]:
            diff['~'][k] = v

    for k in origin:
        if k not in new:
            diff['-'].append(k)

    return diff
