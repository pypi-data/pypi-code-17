# -*- coding: utf-8 -*-

import copy
from datetime import datetime

from fiqs.i18n import _


class Field(object):
    def __init__(self, type, key=None, verbose_name=None, storage_field=None,
                 unit=None, choices=None, data=None, parent=None):
        verbose_name = verbose_name or key
        storage_field = storage_field or key
        choices = choices or ()
        data = data or {}

        self.key = key
        self.type = type
        self.verbose_name = verbose_name
        self.storage_field = storage_field
        self.unit = unit
        self.choices = choices
        self.data = data
        self.parent = parent

    def get_copy(self):
        return self.__class__(
            key=self.key, verbose_name=self.verbose_name, storage_field=self.storage_field,
            unit=self.unit, choices=self.choices, data=self.data, parent=self.parent,
        )

    def __repr__(self):
        if hasattr(self, 'model'):
            return '<{}: {}.{}>'.format(
                self.__class__.__name__,
                self.model.__name__,
                self.key,
            )

        return '<{}: {}>'.format(
                self.__class__.__name__,
                self.key,
        )

    def _set_key(self, key):
        self.key = key
        if not self.verbose_name:
            self.verbose_name = key
        if not self.storage_field:
            self.storage_field = key

    def get_storage_field(self):
        parent_field = self.get_parent_field()
        if not parent_field:
            return self.storage_field

        return '{}.{}'.format(
            parent_field.get_storage_field(),
            self.storage_field,
        )

    def bucket_params(self):
        d = {
            'name': self.key,
            'field': self.get_storage_field(),
        }

        if 'script' in self.data:
            # should we remove field?
            d['script'] = self.data['script'].format('_value')

        if 'size' in self.data:
            size = self.data['size']
            if size == 0:
                size = 2 ** 32 - 1
            d['size'] = size

        return d

    def is_range(self):
        return 'ranges' in self.data

    def _has_pretty_choices(self):
        return self.choices and isinstance(self.choices[0], tuple)

    def choice_keys(self):
        if self._has_pretty_choices():
            return [choice[0] for choice in self.choices]

        if self.choices:
            return self.choices

        if self.is_range():
            return [r['key'] for r in self.data['ranges']]

        raise NotImplementedError()

    def min_key(self):
        if self.data and 'min' in self.data:
            return self.data['min']

        if self.choices:
            return min(self.choice_keys())

    def max_key(self):
        if self.data and 'max' in self.data:
            return self.data['max']

        if self.choices:
            return max(self.choice_keys())

    def get_parent_field(self):
        if not self.parent:
            return None
        return getattr(self.model, self.parent)

    def get_casted_value(self, v):
        return v


class TextField(Field):
    def __init__(self, **kwargs):
        super(TextField, self).__init__('text', **kwargs)


class KeywordField(Field):
    def __init__(self, **kwargs):
        super(KeywordField, self).__init__('keyword', **kwargs)


class DateField(Field):
    def __init__(self, **kwargs):
        super(DateField, self).__init__('date', **kwargs)

    def get_casted_value(self, v):
        # Careful, we lose the milliseconds here
        return datetime.utcfromtimestamp(v / 1000)


class IntegerField(Field):
    def __init__(self, **kwargs):
        super(IntegerField, self).__init__('integer', **kwargs)

    def get_casted_value(self, v):
        return int(v) if v else v


class FloatField(Field):
    def __init__(self, **kwargs):
        super(FloatField, self).__init__('float', **kwargs)

    def get_casted_value(self, v):
        return float(v) if v else v


class ByteField(Field):
    def __init__(self, **kwargs):
        super(ByteField, self).__init__('byte', **kwargs)

    def get_casted_value(self, v):
        return int(v) if v else v


def get_weekdays():
    return [
        (0, _('Monday')),
        (1, _('Tuesday')),
        (2, _('Wednesday')),
        (3, _('Thursday')),
        (4, _('Friday')),
        (5, _('Saturday')),
        (6, _('Sunday')),
    ]


def get_iso_weekdays():
    return [
        (1, _('Monday')),
        (2, _('Tuesday')),
        (3, _('Wednesday')),
        (4, _('Thursday')),
        (5, _('Friday')),
        (6, _('Saturday')),
        (7, _('Sunday')),
    ]


class DayOfWeekField(ByteField):
    def __init__(self, iso=True, **kwargs):
        if iso:
            choices = get_iso_weekdays()
            data = {'min': 1, 'max': 7}
        else:
            choices = get_weekdays()
            data = {'min': 0, 'max': 6}

        kwargs['choices'] = choices
        kwargs['data'] = data

        super(DayOfWeekField, self).__init__(**kwargs)


class HourOfDayField(ByteField):
    def __init__(self, **kwargs):
        kwargs['choices'] = [(i, _('{hour}h').format(hour=i)) for i in range(24)]
        kwargs['data'] = {'min': 0, 'max': 23}

        super(HourOfDayField, self).__init__(**kwargs)


class BooleanField(Field):
    def __init__(self, **kwargs):
        super(BooleanField, self).__init__('boolean', **kwargs)


class NestedField(Field):
    def __init__(self, **kwargs):
        super(NestedField, self).__init__('nested', **kwargs)

    def nested_params(self):
        params = {
            'name': self.key,
            'agg_type': 'nested',
            'path': self.get_storage_field(),
        }
        return params


class ReverseNestedField(Field):
    def __init__(self, **kwargs):
        super(ReverseNestedField, self).__init__('reverse_nested', **kwargs)

    def nested_params(self):
        params = {
            'name': self.key,
            'agg_type': 'reverse_nested',
        }
        # /!\ path must not be provided for root reverse_nested aggregation
        if self.key != 'root':
            params['path'] = self.key

        return params


class FieldWithChoices(Field):
    def __init__(self, field, choices=None):
        choices = choices or ()
        data = copy.deepcopy(field.data)
        return super(FieldWithChoices, self).__init__(
            field.type,
            key=field.key,
            verbose_name=field.verbose_name,
            storage_field=field.storage_field,
            unit=field.unit,
            choices=choices,
            data=data,
            parent=field.parent,
        )


class DataExtendedField(Field):
    def __init__(self, field, **kwargs):
        data = copy.deepcopy(field.data)
        data.update(**kwargs)
        return super(DataExtendedField, self).__init__(
            field.type,
            key=field.key,
            verbose_name=field.verbose_name,
            storage_field=field.storage_field,
            unit=field.unit,
            choices=field.choices,
            data=data,
            parent=field.parent,
        )
