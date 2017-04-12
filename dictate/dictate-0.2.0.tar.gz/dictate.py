#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hashlib import md5


__version__ = '0.2.0'


def _parse_key(k):
    if k.startswith('[') and k.endswith(']'):
        k = int(k[1:-1])
    return k


def _combine_key(keys):
    return '.'.join(k.key for k in keys)


class RKey(object):
    def __init__(self, from_type, key, origin_key=None):
        self.from_type = from_type
        self.key = key
        if origin_key is None:
            self.origin_key = key
        else:
            self.origin_key = origin_key

    @classmethod
    def l(cls, index, origin_key):
        return cls(list, index, origin_key)

    @classmethod
    def d(cls, key):
        return cls(dict, key)


def parse_retrieve_path(path):
    keys = []
    for i in path.split('.'):
        if i.startswith('[') and i.endswith(']'):
            try:
                k = int(i[1:-1])
            except ValueError:
                raise ValueError("`{}` is not a valid key for list".format(i))
            keys.append(RKey.l(k, i))
        else:
            keys.append(RKey.d(i))
    return keys


def retrieve_dict(doc, path):
    """Retrive value from a nested dict, using path like this:
        foo.bar.[0].player
    :raises: KeyError, for not be able to find the value by path
    :raises: ValueError, for invalid path format
    """
    # parse path to keys
    if isinstance(path, list):
        # check path as keys
        keys = path
        for i in keys:
            if not isinstance(i, RKey):
                raise ValueError('{} is not an instance of RKey'.format(i))
    else:
        keys = parse_retrieve_path(path)

    def recurse_dict(d, keys, used):
        try:
            k = keys.pop(0)
        except IndexError:
            return d

        # d must be the same type as k.from_type indicates
        if not isinstance(d, k.from_type):
            used_path = _combine_key(used)
            raise KeyError(
                "Failed to get `{}` after `{}`: `{}` is not type of {}".format(
                    k.origin_key, used_path, used_path, k.from_type))

        try:
            d = d[k.key]
        except IndexError as e:
            used_path = _combine_key(used)
            raise KeyError(
                "Failed to get `{}` after `{}`: {}".format(k.origin_key, used_path, e))
        except KeyError as e:
            used_path = _combine_key(used)
            raise KeyError(
                "Failed to get `{}` after `{}`: {}".format(k.origin_key, used_path, e))

        used.append(k)
        return recurse_dict(d, keys, used)

    return recurse_dict(doc, keys, [])


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
