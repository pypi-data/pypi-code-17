from __future__ import absolute_import, division, print_function, unicode_literals

def merge(list_list):
    merged = [item for sublist in list_list for item in sublist]
    return list(set(merged))

def flatten(nested_list):
    while len(nested_list) > 0 and nested_list[0].__class__ is list:
        nested_list = merge(nested_list)
    return nested_list

def filter_list(filter_function, item_list):
    results = filter(lambda x: filter_function(x), item_list)
    return list(results)

def getprop(obj, str_accessor):
    try:
        props = str_accessor.split(".")
        for prop in props:
            obj = getattr(obj, prop)
        return obj
    except:
        print(obj)
        raise Exception("A context value did not exist. Check your context provider and your filters. Key error: {}".format(str_accessor))

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