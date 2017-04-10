from siftpy._util.helpers import filter_list
from siftpy._exceptions import ValidationException

class OperationMethodResolver(object):
    methods = {
        "count": lambda k: len(list(k))
    }

    def __init__(self, context_provider):
        self.__context_provider = context_provider

    def resolve(self, method_name):
        method = self.methods.get(method_name, False)
        if not method:
            method = self.__context_provider.resolve_operation(method_name)
            if not method:
                raise Exception("No method was returned from resolve_operation")
        return method


class Reducer(object):

    def __init__(self, context_provider):
        self.__operation_method_resolver = OperationMethodResolver(context_provider)

    def reduce(self, object_set, filters, as_operation, returning_property=None):
        results = self.__filter(object_set, filters)
        if as_operation:
            return self.__operate(results, returning_property)
        elif returning_property is not None:
            results = self.__convert(results, returning_property)        
        return results

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

    def __operate(self, object_set, method_name): 
        method = self.__operation_method_resolver.resolve(method_name)
        return [method(object_set)]