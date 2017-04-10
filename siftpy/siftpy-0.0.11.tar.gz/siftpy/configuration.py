from __future__ import absolute_import, division, print_function, unicode_literals

from siftpy._util.printers import SiftPrinter

class SiftFilterType(object):
    Evaluation = "evaluation"
    Context = "context"
    Relative = "relative"

class SiftFilterOperator(object):
    LessThan = "<"
    LessThanOrEqualTo = "<="
    EqualTo = "=="
    GreaterThanOrEqualTo = ">="
    GreaterThan = ">"
    NotEqualTo = "!="
    IsNone = "is_none"
    IsNotNone = "is_notnone"

    #Relatives
    InTopCount = "in_top"
    InBottomCount = "in_bottom"
    AboveAvg = "above_avg"
    BelowAvg = "below_avg"

class SiftFilterKey(object):
    Operator = "operator"
    Property = "property"
    ComparisonValue = "comparison_value"
    FilterType = "filter_type"

class SiftAggregationType(object):
    Combine = "combine"
    ChooseSource = "choose_source"
    ChooseElement = "choose_element"
    Operation = "operation"

class SiftPropertyKey(object):
    Id = "id"
    ReturningObjectProperty = "returning_object_property"
    Count = "count"
    ContextSource = "context_source"
    Filters = "filters"
    Sifts = "sifts"
    Description = "description"
    AggregationType = "aggregation_type"

class SiftPropertyDefaults(object): pass 
setattr(SiftPropertyDefaults, SiftPropertyKey.Id, lambda: None)
setattr(SiftPropertyDefaults, SiftPropertyKey.ReturningObjectProperty, lambda: None)
setattr(SiftPropertyDefaults, SiftPropertyKey.Count, lambda: None)
setattr(SiftPropertyDefaults, SiftPropertyKey.ContextSource, lambda: None)
setattr(SiftPropertyDefaults, SiftPropertyKey.Filters, lambda: [])
setattr(SiftPropertyDefaults, SiftPropertyKey.Sifts, lambda: [])
setattr(SiftPropertyDefaults, SiftPropertyKey.Description, lambda: "")
setattr(SiftPropertyDefaults, SiftPropertyKey.AggregationType, lambda: SiftAggregationType.Combine)

class SiftFilterCacheKey(object):
    ForNone = "$.none"


class SiftConfiguration(object):
    def __init__(self):
        self.SiftFilterType         = SiftFilterType
        self.SiftFilterOperator     = SiftFilterOperator
        self.SiftFilterKey          = SiftFilterKey
        self.SiftPropertyKey        = SiftPropertyKey
        self.SiftFilterCacheKey     = SiftFilterCacheKey
        self.SiftAggregationType    = SiftAggregationType
        self.SiftPropertyDefaults   = SiftPropertyDefaults

        self.SiftPrinter            = SiftPrinter

        self.CacheFilterFunctions   = True