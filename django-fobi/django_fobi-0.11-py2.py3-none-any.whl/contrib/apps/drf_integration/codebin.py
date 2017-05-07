# This should be removed once ready.

# *************************************************************************
# ***************************** NoneField field ***************************
# *************************************************************************

import six

from django.utils.safestring import mark_safe

from rest_framework.fields import Field, empty


class NoneField(Field):
    """NoneField."""

    default_error_messages = {}
    initial = ''
    default_empty_html = ''

    def __init__(self, **kwargs):
        self.allow_blank = True
        self.trim_whitespace = kwargs.pop('trim_whitespace', True)
        super(NoneField, self).__init__(**kwargs)

    def run_validation(self, data=empty):
        # Test for the empty string here so that it does not get validated,
        # and so that subclasses do not need to handle it explicitly
        # inside the `to_internal_value()` method.
        if data == '' \
                or (self.trim_whitespace
                    and six.text_type(data).strip() == ''):

            return ''
        return super(NoneField, self).run_validation(data)

    def to_internal_value(self, data):
        # We're lenient with allowing basic numerics to be coerced into
        # strings, but other types should fail. Eg. unclear if booleans
        # should represent as `true` or `True`, and composites such as lists
        # are likely user error.
        _not_isinstance_str_int_float = not isinstance(
            data, six.string_types + six.integer_types + (float,)
        )
        if isinstance(data, bool) or _not_isinstance_str_int_float:
            self.fail('invalid')
        value = six.text_type(data)
        return value.strip() if self.trim_whitespace else value

    def to_representation(self, value):
        return mark_safe(six.text_type(value))
