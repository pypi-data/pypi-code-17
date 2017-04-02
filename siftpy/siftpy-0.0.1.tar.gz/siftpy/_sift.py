from __future__ import absolute_import, division, print_function, unicode_literals

from siftpy._util.helpers import (merge, flatten, filter_list) 
from siftpy._util.printers import SiftPrinter

class SiftResult(object):
    def __init__(self, data):
        self.data = data


class Sift(object): 

    def __init__(self, config):
        self.config = config
        self.__printer = self.config.SiftPrinter(self.config)

    @property
    def __is_leaf(self):
        return len(self.sifts) == 0

    @property
    def __is_root(self):
        return self.parent is None

    def print(self):
        self.__printer.print(self)

    def evaluate(self):
        '''Returns an array of matching object instance sets'''        
        branch_results = self.__get_branch_results() 
        if self.merge_children:
            flattened_results = flatten(branch_results)
            return SiftResult(self.__filter_and_convert(flattened_results))
        else:
            return SiftResult(list(map(self.__filter_and_convert, branch_results)))

    def __get_branch_results(self):
        if self.__is_leaf:
            return self.__get_leaf_results()
        return self.__evaluate_child_sifts() 

    def __get_leaf_results(self):
        assert self.__is_root or self.merge_children
        return getattr(self.context_provider.context, self.context_source)

    def __evaluate_child_sifts(self):
        return [sift.evaluate().data for sift in self.sifts]

    def __filter_and_convert(self, result_set):
        filtered = self.__filter(result_set)
        if self.returning_object_property is not None:
            return self.__convert(filtered)
        return (filtered)

    def __filter(self, object_list):
        for filter_fn in self.filters:
            object_list = filter_list(filter_fn, object_list)
        return object_list

    def __convert(self, result_set): 
        new_result_set = []
        for result in result_set:
            prop = getattr(result, self.returning_object_property)
            if prop:
                new_result_set.append(prop)
        return new_result_set