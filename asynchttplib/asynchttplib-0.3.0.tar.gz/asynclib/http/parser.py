from asynclib.http.error import RequestParamsError, BaseError


class ValidationError(BaseError):

    def __init__(self, code):
        super(ValidationError, self).__init__(code=code, description='Validation error')


class ValidatorErrorCodes(object):
    VALUE_REQUIRED = 'VALUE_REQUIRED'
    VALUE_TYPE_ERROR = 'VALUE_TYPE_ERROR'


def raise_if(condition, code):
    if condition:
        raise ValidationError(code=code)


def raise_if_not_instance(value, cls):
    raise_if(not isinstance(value, cls), ValidatorErrorCodes.VALUE_TYPE_ERROR)


class Field(object):

    def __init__(self, required=False):
        self.required = required

    async def deserialize(self, value):
        if self.required and value is None:
            raise ValidationError(ValidatorErrorCodes.VALUE_REQUIRED)
        return value


class String(Field):

    async def deserialize(self, value):
        value = await super(String, self).deserialize(value)
        if value is None:
            return None
        raise_if_not_instance(value, (bytes, str))
        if isinstance(value, bytes):
            value = value.decode('utf-8')
        return value


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
