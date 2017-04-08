import datetime

from asynclib.http.error import RequestParamsError, BaseError


class ValidationError(BaseError):

    def __init__(self, code):
        super(ValidationError, self).__init__(code=code, description='Validation error')


class ValidatorErrorCodes(object):
    VALUE_REQUIRED = 'VALUE_REQUIRED'
    VALUE_TYPE_ERROR = 'VALUE_TYPE_ERROR'
    ENUM_ERROR = 'ENUM_ERROR'


def raise_if(condition, code):
    if condition:
        raise ValidationError(code=code)


def raise_if_not_instance(value, cls):
    raise_if(not isinstance(value, cls), ValidatorErrorCodes.VALUE_TYPE_ERROR)


class Validator(object):

    async def validate(self, value):
        raise NotImplementedError()



class OneOf(Validator):

    def __init__(self, choices):
        self.choices = choices

    async def validate(self, value):
        raise_if(value not in self.choices, ValidatorErrorCodes.ENUM_ERROR)


class Field(object):

    def __init__(self, required=False, validators=None):
        self.required = required
        self.validators = validators if validators is not None else []

    async def deserialize(self, value):
        if self.required and value is None:
            raise ValidationError(ValidatorErrorCodes.VALUE_REQUIRED)
        value = await self._deserialize(value)
        await self.validate(value)
        return value

    async def _deserialize(self, value):
        return value

    async def validate(self, value):
        for validator in self.validators:
            await validator.validate(value)


class DefaultTypeField(Field):

    def __init__(self, _type, required=False, validators=None):
        self._type = _type
        super(DefaultTypeField, self).__init__(required=required, validators=validators)

    async def _deserialize(self, value):
        if value is None:
            return None
        raise_if_not_instance(value, self._type)
        return value


class String(Field):

    async def _deserialize(self, value):
        if value is None:
            return None
        raise_if_not_instance(value, (bytes, str))
        if isinstance(value, bytes):
            value = value.decode('utf-8')
        await self.validate(value)
        return value


class Integer(DefaultTypeField):
    def __init__(self, required=False, validators=None):
        super(Integer, self).__init__(int, required=required, validators=validators)


class Float(DefaultTypeField):

    def __init__(self, required=False, validators=None):
        super(Float, self).__init__(float, required=required, validators=validators)


class Datetime(String):

    async def _deserialize(self, value):
        value = await super(Datetime, self)._deserialize(value)
        return datetime.datetime.strptime(value[:19], '%Y-%m-%dT%H:%M:%S')



async def parse_args(args, arg_map):
    """
    :type args: dict
    :type arg_map: dict
    """
    serialized = {}
    error_map = {}
    for key, field in arg_map.items():
        try:
            value = await field.deserialize(args.get(key))
            serialized[key] = value
        except BaseError as error:
            error_map[key] = error.code
    if error_map:
        raise RequestParamsError(error_map)
    return serialized
