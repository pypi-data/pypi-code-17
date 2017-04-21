class TooManyFieldsError(Exception):
    pass

class TooLessFieldsError(Exception):
    pass

class UnexpectedFieldError(Exception):
    pass

class RedisNaming(object):
    def __init__(self, key_field=None, key_fields=None, value_field=None, value_fields=None):
        # TODO: validate the parameter values
        if self.key_fields is None:
            self.key_fields = [key_field]
        if self.value_fields is None:
            self.value_fields = [value_field]

    def build_key(**kargs)
        """Build the key name"""
        # TODO: validate the parameter values
        # TODO: support args param

        key = ""
        for key_field in self.key_fields:
            key += key_field
            key += kargs[key_field]
        if len(self.value_fields) == 1:
            key += value_fields[0]
        return key

    def build_value(**kargs)
        # TODO: validate the parameter values
        # TODO: support args param

        if len(self.value_fields) == 1:
            return kargs[self.value_fields]
        value = ""
        for value_field in self.value_fields:
            value += value_field
            value += kargs[value_field]
        return value

