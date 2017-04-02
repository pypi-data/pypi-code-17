# coding=utf-8
import functools
from bson import ObjectId
from bson.errors import InvalidId
from marshmallow import fields, validate, Schema
from webargs import argmap2schema
import aiohttp.web

from asynclib.http.error import BaseError

fields = fields
validate = validate
Schema = Schema


class ErrorBodySchema(Schema):
    description = fields.String()
    code = fields.String()
    body = fields.Dict()


async def throwable(func):

    async def _(*args, **kwargs):
        try:
            result = await func(*args, **kwargs)
            return result
        except BaseError as error:
            body = ErrorBodySchema().dumps(error.map()).data
            return aiohttp.web.Response(body=body, status=error.status)

    return _


def use_schema(schema):

    async def decorator(func):
        func.schema = schema

        async def wrapper(*args, **kwargs):
            result = await func(*args, **kwargs)
            body = schema().dumps(result).data
            return aiohttp.web.Response(body=body, status=200)
        return wrapper

    return decorator


class Nested(fields.Nested):
    """
    Кастомное поле Nested, для использования с множественными схемами
    Если указан callback - nested должен быть словарем
    callback принимает в качестве аргумента результат и возвращает ключ словаря nested (какую схему использовать)
    """

    def __init__(self, nested, callback=None, *args, **kwargs):
        self.callback = None
        if callback is not None:
            self.callback = callback
            nested = {a: self.__argmap2schema(b) for a, b in nested.items()}
            self._nested = nested
        else:
            nested = self.__argmap2schema(nested)
        super(Nested, self).__init__(nested, *args, **kwargs)

    def __argmap2schema(self, schema):
        if isinstance(schema, dict):
            schema = argmap2schema(schema)
        return schema

    def _serialize(self, nested_obj, attr, obj):
        if self.callback is not None:
            self.__schema = None
            self.nested = self._nested[self.callback(nested_obj)]
        result = super(Nested, self)._serialize(nested_obj, attr, obj)
        if self.callback is not None:
            self.nested = self._nested
        return result


class MongoId(fields.String):
    def _serialize(self, value, attr, obj):
        return super(MongoId, self)._serialize(value, attr, obj)

    def _deserialize(self, value, attr, data):
        value = super(MongoId, self)._deserialize(value, attr, data)
        try:
            return ObjectId(value)
        except InvalidId:
            self.fail('invalid')


class DateTimeReplaced(fields.DateTime):
    def _serialize(self, value, attr, obj):
        value = value.replace(microsecond=0) if value is not None else None
        return super(DateTimeReplaced, self)._serialize(value, attr, obj)

    def _deserialize(self, value, attr, obj):
        return super(DateTimeReplaced, self)._serialize(value, attr, obj)


class OKSchema(Schema):
    ok = fields.Boolean()


def make_list_schema(schema, *args, **kwargs):
    class _Shema(Schema):
        total = fields.Integer()
        objects = fields.List(Nested(schema, *args, **kwargs))

    return _Shema


skip_limit_args = {'skip': fields.Integer(), 'limit': fields.Integer()}

fields.MongoId = MongoId