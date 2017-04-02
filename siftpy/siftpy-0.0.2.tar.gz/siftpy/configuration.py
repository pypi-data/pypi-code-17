from __future__ import absolute_import, division, print_function, unicode_literals

from siftpy._util.printers import SiftPrinter

class SiftFilterType(object):
    Evaluation = "evaluation"
    Context = "context"

class SiftFilterOperator(object):
    LessThan = "<"
    LessThanOrEqualTo = "<="
    EqualTo = "=="
    GreaterThanOrEqualTo = ">="
    GreaterThan = ">"
    NotEqualTo = "!="

class SiftFilterKey(object):
    Operator = "operator"
    Property = "property"
    ComparisonValue = "comparison_value"
    FilterType = "filter_type"

class SiftPropertyKey(object):
    Id = "id"
    MergeChildren = "merge_children"
    ReturningObjectProperty = "returning_object_property"
    Count = "count"
    ContextSource = "context_source"
    Filters = "filters"
    Sifts = "sifts"

class SiftFilterCacheKey(object):
    ForNone = "$.none"


class SiftConfiguration(object):
    def __init__(self):
        self.SiftFilterType         = SiftFilterType
        self.SiftFilterOperator     = SiftFilterOperator
        self.SiftFilterKey          = SiftFilterKey
        self.SiftPropertyKey        = SiftPropertyKey
        self.SiftFilterCacheKey     = SiftFilterCacheKey

        self.SiftPrinter            = SiftPrinter

        self.CacheFilterFunctions   = True