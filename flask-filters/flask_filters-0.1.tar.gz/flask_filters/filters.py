"""Implement filter class which will handle filtering
"""
from flask_restful import reqparse
from datetime import datetime

FILTER_UNDERSCORE_KEYWORDS = ['__like', '__gt', '__gte', '__lt', '__lte']


class Filters(object):
    """Generic class to handle filtering of all models
    """
    model = None
    fields = None
    session = None

    def __init__(self):
        self.session_query = None
        self.filter_args = None
        self._set_filter_args()
        self._set_queryset(self.session.query(self.model))

    def _set_queryset(self, queryset):
        self.session_query = queryset

    def get_queryset(self):
        return self.session_query

    def _set_filter_args(self):
        """
        # Create filter arguments for fields
        :return:
        """
        parser = reqparse.RequestParser()
        for field_name in self.fields:
            if type(field_name) is tuple:
                field_name, field_type = field_name
            else:
                field_type = eval('self.model.%s.type.python_type' % field_name)

            parser.add_argument(field_name, type=field_type)

            if field_type == str:
                # Add support for like keyword
                parser.add_argument('%s__like' % field_name, type=field_type)

            elif field_type in (int, datetime):
                parser.add_argument('%s__gt', type=field_type)
                parser.add_argument('%s__gte', type=field_type)
                parser.add_argument('%s__lt', type=field_type)
                parser.add_argument('%s__lte', type=field_type)

        self.filter_args = parser.parse_args()

    def _parse_filter_args(self):
        """Parse kwargs and return dict
        :return:
        """
        model_kwargs = {}
        custom_kwargs = {}
        underscore_kwargs = {}
        for key, value in self.filter_args.iteritems():
            if value:
                if hasattr(self.model, key):
                    """Check the key is the model argument
                    """
                    model_kwargs[key] = self.filter_args[key]
                elif any(key.endswith(i) for i in FILTER_UNDERSCORE_KEYWORDS):
                    underscore_kwargs[key] = value
                else:
                    custom_kwargs[key] = self.filter_args[key]
        return model_kwargs, custom_kwargs, underscore_kwargs

    def get_results(self):
        """Method to filter the result based on parser argument
        1. Separate out the custom argument and model argument
        :return:
        """
        model_kwargs, custom_kwargs, underscore_kwargs = self._parse_filter_args()
        obj_list = self.session_query.filter_by(**model_kwargs)
        for underscore_arg in underscore_kwargs:
            if underscore_arg.endswith('like'):
                # It's the like keyword
                field_name = underscore_arg.replace('__like',  '')
                field_execute_string = 'self.model.{0}.like("%{1}%")'.format(field_name,
                                                                           underscore_kwargs[underscore_arg])
                obj_list = obj_list.filter(eval(field_execute_string))

        self._set_queryset(obj_list)

        for custom_key in custom_kwargs:
            """For custom key call the custom method which is implemented in subclass
            example:
            class MyFilter(Filters):
                fields = ('name', 'recent')
                # recent is custome field
                def get_recent(self, value):
                    // Query to operate on custom value
            """
            function_name = 'get_%s'%custom_key
            obj_list = eval('self.%s(%s)' % (function_name, custom_kwargs[custom_key]))
            self._set_queryset(obj_list)

        return obj_list.all()
