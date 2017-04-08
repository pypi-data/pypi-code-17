from siftpy._util.helpers import filter_list

class Reducer(object):

    def reduce(self, object_set, filters, returning_property=None):
        filtered = self.__filter(object_set, filters)
        if returning_property is not None:
            return self.__convert(filtered, returning_property)
        return filtered

    def __filter(self, object_set, filters):
        for filter_fn in filters:
            object_set = filter_list(filter_fn, object_set)
        return object_set

    def __convert(self, object_set, returning_property): 
        new_object_set = []
        for result in object_set:
            prop = getattr(result, returning_property)
            if prop:
                new_object_set.append(prop)
        return new_object_set