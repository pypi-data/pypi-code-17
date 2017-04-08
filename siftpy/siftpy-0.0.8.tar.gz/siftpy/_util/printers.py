from __future__ import absolute_import, division, print_function, unicode_literals

class SiftPrinter(object):
    padding_per_level = 6
    assert padding_per_level % 2 is 0
    
    def __init__(self, config):
        self.config = config
        self.fields = (
            self.config.SiftPropertyKey.Id,
            self.config.SiftPropertyKey.AggregationType,
            self.config.SiftPropertyKey.ReturningObjectProperty,
            self.config.SiftPropertyKey.Count
        )

    def print(self, root_sift):
        print(self.get_str(root_sift))

    def get_str(self, root_sift):
        return self.__print_repr(root_sift, 0)

    def __print_repr(self, sift, padding):
        text = ""
        pad_str = self.__get_indent(padding)
        text += pad_str + "[{}]".format(sift.__class__.__name__) + "\n"

        for field in self.fields:  
            text += self.__print_field_with_padding(sift, pad_str, field) + "\n"

        text += "{}{}: {}\n".format(pad_str, self.config.SiftPropertyKey.ContextSource, sift.original_source.get(self.config.SiftPropertyKey.ContextSource, "None"))


        filters_str = ",  Dynamic: [" + str([ f for f in sift.original_source[self.config.SiftPropertyKey.Filters]]) + "]"
        text += "{}{}: {}\n".format(pad_str, self.config.SiftPropertyKey.Filters, filters_str)

        for sift in sift.sifts:
            new_padding = padding + self.padding_per_level
            text += self.__print_repr(sift, new_padding)

        return text

    def __print_field_with_padding(self, sift, pad_str, field_name):
        text = "{}{}: {}".format(pad_str, field_name, str(getattr(sift, field_name)))        
        return text

    def __get_indent(self, padding):
        return "".join([" " for _ in range(0, padding)])

class SiftTranslator(object):

    def __init__(self, config):
        self.config = config

    def translate(self, sift):
        base_text = "Either" if sift.is_choice else "All items from"

        filter_descriptions = [self.__context_filter_description(filter) for filter in sift.original_source[self.config.SiftPropertyKey.Filters]]
        filter_text = "where " + ", ".join(filter_descriptions) if filter_descriptions else ""

        if not sift.sifts:
            source = sift.context_source
        else:
            child_str = []
            for child in sift.sifts:
                child_str.append("(" + self.translate(child)+")")
            source = " {}".format(" OR ".join(child_str) )
            source = base_text + source
            
        return "{source} {filter_text}".format(base_text=base_text, source=source, filter_text=filter_text)

    def __context_filter_description(self, filter):
        return "{property} {operator} {comparison_value}".format(
                property=filter["property"],
                operator=filter["operator"],
                comparison_value=filter.get("comparison_value", None))