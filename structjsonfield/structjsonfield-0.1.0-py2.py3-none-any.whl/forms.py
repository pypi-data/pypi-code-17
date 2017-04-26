from django import forms
from django.contrib.postgres.forms import JSONField
from django.core.exceptions import ImproperlyConfigured
import json
from collections import OrderedDict
from . import widgets


class StructJSONField(JSONField):
    def __init__(self, structure, add_label=None, multiple=True, **kwargs):
        if not multiple:
            raise NotImplementedError("At this point the StructJSONField only supports multi-line JSON input")

        self.structure = structure
        self.multiple = multiple
        self.add_label = add_label if add_label else "Add another"
        self._verify_structure()

        if 'widget' not in kwargs:
            kwargs['widget'] = widgets.StructJSONInput(structure=self.structure,
                                                       add_label=self.add_label)

        super(StructJSONField, self).__init__(**kwargs)

    def clean(self, value):
        if value in self.empty_values:
            return
        try:
            value = json.loads(value)
        except ValueError:
            raise forms.ValidationError(
                self.error_messages['invalid'],
                code='invalid',
                params={'value': value},
            )

        for line in value:
            value_keys = set(line.keys())
            unknown_columns = value_keys - set(self.structure.keys())
            if unknown_columns:
                raise forms.ValidationError(
                    "Unkown columns in the data: {}".format(unknown_columns))

            missing_required = set(self._required_columns) - value_keys
            if missing_required:
                raise forms.ValidationError(
                    "The following fields are required and missing: {}".format(missing_required))

            for column, c_value in line.items():
                field = self.structure[column]
                if field.required and not c_value:
                    raise forms.ValidationError(
                        "The following JSON column is required: {}".format(column))
                c_value = field.clean(c_value)

        return value

    def _filter_and_sort(self, line):
        return OrderedDict((key, line.get(key, None)) for key in self._structure_keys)

    def prepare_value(self, value):
        return [self._filter_and_sort(line) for line in value]

    def _verify_structure(self):
        self._required_columns = []

        for name, field in self.structure.items():
            if not isinstance(field, forms.Field):
                raise ImproperlyConfigured(
                    "Column {} is not of type django.forms.Field".format(name))

            if field.required:
                self._required_columns.append(name)

        self._structure_keys = tuple(self.structure.keys())
