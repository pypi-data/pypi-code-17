from __future__ import absolute_import, division, print_function, unicode_literals
from siftpy._util.helpers import (merge, flatten,) 
from siftpy._util.printers import SiftTranslator
from siftpy._exceptions import ValidationException, FlowException
from siftpy._choice import Choice
from siftpy._reducer import Reducer
from siftpy._context_extractor import ContextExtractor

class Sift(object):    

    def __init__(self, config, parent, context_provider, filter_provider):
        self.config = config
        self.__printer = self.config.SiftPrinter(self.config)
        self.__translator = SiftTranslator(self.config)
        self.__context_extractor = ContextExtractor()
        self.context_provider = context_provider
        self.__reducer = Reducer(self.context_provider)
        self.__choice_results = None      
        self.__answered = False  
        self.filter_provider = filter_provider
        self.parent = parent

    def print(self):
        self.__printer.print(self)
        print(self.__translator.translate(self))

    @property
    def is_choice(self):
        return self.aggregation_type in (
            self.config.SiftAggregationType.ChooseSource,
            self.config.SiftAggregationType.ChooseElement,)

    def get_choice(self):
        for sift in self.sifts:
            choice = sift.get_choice()
            if choice:
                return choice
        if self.is_choice and not self.__answered:
            if self.aggregation_type == self.config.SiftAggregationType.ChooseElement:
                options = self.results()
                if options:
                    return Choice(options, self.__answer, None)  
            elif self.aggregation_type == self.config.SiftAggregationType.ChooseSource:
                options = self.sifts
                if options:
                    return Choice(options, self.__answer, "description")  

    def __answer(self, results):
        if not self.is_choice:
            raise FlowException("You cannot 'answer' a result sift")
        self.__answered = True
        if self.aggregation_type == self.config.SiftAggregationType.ChooseElement:
            self.__choice_results = results
        else:
            self.sifts = [sift for sift in self.sifts if sift in results]

    def results(self):
        if self.__choice_results is not None:
            return self.__choice_results
        as_operation = self.aggregation_type == self.config.SiftAggregationType.Operation
        return self.__reducer.reduce(self.__branch_results, self.filters, as_operation, self.returning_object_property)

    @property
    def __branch_results(self):
        if self.__is_leaf:
            return self.__leaf_results
        return flatten(self.__child_sift_results)

    @property
    def __is_leaf(self): return len(self.sifts) == 0  

    @property
    def __leaf_results(self):
        return self.__context_extractor.list(self.context_provider, self.context_source)

    @property
    def __child_sift_results(self):
        return [sift.results() for sift in self.sifts]

