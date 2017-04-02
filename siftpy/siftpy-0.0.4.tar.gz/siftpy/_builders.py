from __future__ import absolute_import, division, print_function, unicode_literals

from siftpy._sift import Sift
from siftpy._providers import FilterProvider
from siftpy.configuration import SiftConfiguration

class SiftBuilder(object):

    def __init__(self, config=None):
        self.config = config or SiftConfiguration()

    def build(self, dictionary, context_provider, filter_provider=None, parent_sift=None):
        sift = Sift(self.config)
        filter_provider = filter_provider or FilterProvider(self.config)
        self.__init_fields(dictionary, context_provider, filter_provider, sift)
        sift.context_provider = context_provider
        sift.parent = parent_sift
        return sift

    def __init_fields(self, dictionary, context_provider, filter_provider, sift):
        self.__init_source(dictionary, sift)
        self.__init_id(dictionary, sift)
        self.__init_merge_children(dictionary, sift)
        self.__init_context_source(dictionary, sift)
        self.__init_returning_object_property( dictionary, sift)
        self.__init_count(dictionary, sift)
        self.__init_filters(dictionary, sift, filter_provider, context_provider)
        self.__init_sifts(dictionary, sift, context_provider, filter_provider)

    def __init_source(self, dictionary, sift):
        sift.source = dictionary

    def __init_id(self, dictionary, sift):
        sift.id = dictionary.get(self.config.SiftPropertyKey.Id, None)

    def __init_merge_children(self, dictionary, sift):
        sift.merge_children = dictionary[self.config.SiftPropertyKey.MergeChildren]

    def __init_context_source(self, dictionary, sift):
        sift.context_source = dictionary.get(self.config.SiftPropertyKey.ContextSource, None)

    def __init_returning_object_property(self, dictionary, sift):
        sift.returning_object_property = dictionary.get(self.config.SiftPropertyKey.ReturningObjectProperty, None)

    def __init_count(self, dictionary, sift):
        sift.count = dictionary.get(self.config.SiftPropertyKey.Count, None)
        
    def __init_filters(self, dictionary, sift, filter_provider, context_provider):  
        filter_set = dictionary.get(self.config.SiftPropertyKey.Filters, [])
        filters = [filter_provider.resolve(obj_filter, context_provider) for obj_filter in filter_set]
        sift.filters = filters

    def __init_sifts(self, dictionary, sift, context_provider, filter_provider):
        sift_set = dictionary.get(self.config.SiftPropertyKey.Sifts, [])
        sift.sifts = [self.build(sift_data, context_provider, filter_provider=filter_provider, parent_sift=sift) for sift_data in sift_set]
