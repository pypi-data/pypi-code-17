from __future__ import absolute_import, division, print_function, unicode_literals

from siftpy._sift import Sift
from siftpy._providers import FilterProvider
from siftpy.configuration import SiftConfiguration
from siftpy._validators import SiftValidator


class SiftBuilder(object):

    def __init__(self, config=None):
        self.config = config or SiftConfiguration()
        self.validator = SiftValidator(self.config)

    def build(self, dictionary, context_provider, filter_provider=None, parent_sift=None):
        self.validator.validate(dictionary)
        filter_provider = filter_provider or FilterProvider(self.config)
        sift = Sift(self.config, parent_sift, context_provider, filter_provider)
        self.__init_fields(dictionary, context_provider, filter_provider, sift)
        return sift

    def __init_fields(self, dictionary, context_provider, filter_provider, sift):
        self.__init_original_source(dictionary, sift)
        self.__init_id(dictionary, sift)
        self.__init_description(dictionary, sift)
        self.__init_context_source(dictionary, sift)
        self.__init_returning_object_property( dictionary, sift)
        self.__init_count(dictionary, sift)
        self.__init_filters(dictionary, sift, filter_provider, context_provider)
        self.__init_aggregation_type(dictionary, sift)
        self.__init_sifts(dictionary, sift, context_provider, filter_provider)

    def __init_original_source(self, dictionary, sift):
        sift.original_source = dictionary

    def __init_id(self, dictionary, sift):
        key = self.config.SiftPropertyKey.Id
        sift.id = dictionary.get(key, self.__default(key))

    def __init_aggregation_type(self, dictionary, sift):       
        key = self.config.SiftPropertyKey.AggregationType 
        sift.aggregation_type = dictionary.get(key, self.__default(key))

    def __init_description(self, dictionary, sift):
        key = self.config.SiftPropertyKey.Description 
        sift.description = dictionary.get(key, self.__default(key))

    def __init_context_source(self, dictionary, sift):
        key = self.config.SiftPropertyKey.ContextSource 
        sift.context_source = dictionary.get(key, self.__default(key))

    def __init_returning_object_property(self, dictionary, sift):
        key = self.config.SiftPropertyKey.ReturningObjectProperty 
        sift.returning_object_property = dictionary.get(key, self.__default(key))

    def __init_count(self, dictionary, sift):
        key = self.config.SiftPropertyKey.Count 
        sift.count = dictionary.get(key, self.__default(key))
        
    def __init_filters(self, dictionary, sift, filter_provider, context_provider):  
        key = self.config.SiftPropertyKey.Filters 
        filter_set = dictionary.get(key, self.__default(key))
        filters = [filter_provider.resolve(obj_filter, context_provider) for obj_filter in filter_set]
        sift.filters = filters

    def __init_sifts(self, dictionary, sift, context_provider, filter_provider):
        key = self.config.SiftPropertyKey.Sifts 
        sift_set = dictionary.get(key, self.__default(key))
        sift.sifts = [self.build(sift_data, context_provider, filter_provider=filter_provider, parent_sift=sift) for sift_data in sift_set]

    def __default(self, key):
        return getattr(self.config.SiftPropertyDefaults, key)()
