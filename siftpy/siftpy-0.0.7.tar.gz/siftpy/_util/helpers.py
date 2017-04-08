from __future__ import absolute_import, division, print_function, unicode_literals
from siftpy._exceptions import PropertyDoesNotExistException, ValidationException

def intop(item, value, itemlist):
    sort = sorted(itemlist, reverse=True)
    return sort.index(item) < value

def inbottom(item, value, itemlist):
    sort = sorted(itemlist)
    return sort.index(item) < value

def aboveavg(item, value, itemlist):
    if value is not None:
        raise ValidationException("Relative filters based on average should have no comparison value.")
    if not itemlist:
        return False;
    avg = sum(itemlist)/float(len(itemlist))
    return item >= avg


def merge(list_list):
    merged = [item for sublist in list_list for item in sublist]
    return list(set(merged))


def flatten(nested_list):
    while len(nested_list) > 0 and nested_list[0].__class__ is list:
        nested_list = merge(nested_list)
    return nested_list


def filter_list(filter_function, item_list):
    results = filter(lambda x: filter_function(x, item_list), item_list)
    return list(results)


def getprop(obj, str_accessor):
    try:
        props = str_accessor.split(".")
        for prop in props:
            obj = getattr(obj, prop)
        return obj
    except Exception as e:
        raise PropertyDoesNotExistException("A property value did not exist. Check your objects, context provider, or filters. Key error: {}. Original access exception: {}".format(str_accessor, str(e)))


class DictWrapper(dict):

    def __init__(self, data=None):
        self.data = data or {}

    def __getattr__(self, name):
        data = self.data.get(name, None)
        if self.__is_dict_or_none(data):
            self.data[name] = DictWrapper(data)
            return self.data[name]
        else:
            return data

    def __setattribute__(self, name, value):
        self.data[name] = value
        return value

    def __is_dict_or_none(self, data):
        return data is None or data.__class__ == dict