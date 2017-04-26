import datetime
from abc import abstractmethod


class Field(object):
    attribute = None
    default = None

    def __init__(self, attribute=None, default=None):
        self.attribute = attribute
        self.default = default

    @abstractmethod
    def format(self, value): pass


class StringField(Field):
    """
    字符串类型字段
    """

    def format(self, value):
        if value is None:
            return self.default
        try:
            return str(value)
        except TypeError:
            return self.default


class FloatField(Field):
    """
    浮点型字段
    """

    def format(self, value):
        try:
            return float(value)
        except TypeError:
            return self.default


class IntegerField(Field):
    """
    整型字段
    """

    def format(self, value):
        try:
            return int(value)
        except TypeError:
            return self.default


class BooleanField(Field):
    """
    布尔类型字段
    """

    def format(self, value):
        if isinstance(value, str):
            return value.upper() == 'TRUE'
        if value:
            return True
        else:
            return False


class DateTimeField(Field):
    """
    时间类型字段
    """

    def __init__(self, attribute=None, dt_format=None, default=None):
        super().__init__(attribute, default)
        if dt_format is None:
            self.dt_format = '%Y-%m-%d %H:%M:%S'
        else:
            self.dt_format = dt_format

    def format(self, value):
        if isinstance(value, datetime.datetime):
            try:
                return datetime.datetime.strftime(value, self.dt_format)
            except ValueError:
                return self.default


def serialize(data, fields):
    """
    整理数据
    :param data: 
    :param fields: 
    :return: 
    """
    if isinstance(data, list):
        results = []
        for item in data:
            results.append(serialize(item, fields))
        return results
    elif isinstance(data, object):
        return _serialize_obj(data, fields)


def _serialize_obj(data, fields):
    """
    整理数据
    :param data: 
    :param fields: 
    :return: 
    """
    if type(data) == dict:
        return _serialize_dict(data, fields)
    result = {}
    for key, field in fields.items():
        if field.attribute:
            result[key] = field.format(data.__getattribute__(field.attribute))
        else:
            result[key] = field.format(data.__getattribute__(key))
    return result


def _serialize_dict(data, fields):
    """
    整理数据
    :param data: 
    :param fields: 
    :return: 
    """
    result = {}
    for key, field in fields.items():
        if field.attribute:
            result[key] = field.format(data.get(field.attribute))
        else:
            result[key] = field.format(data.get(key))
    return result
