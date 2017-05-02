# -*- coding:utf-8 -*-

class ValidationError(Exception):

    def __init__(self, message, code=None, params=None):

        super(ValidationError, self).__init__(message, code, params)
        self.message = message
        self.params = params

    def __str__(self):
        return self.message.format(**self.params)


class ImproperlyConfigured(Exception):
    """Lawes is somehow improperly configured"""
    pass


class MultipleObjectsReturned(Exception):
    """The query returned multiple objects when only one was expected."""
    pass


class DoesNotExist(Exception):
    """The query returned None objects when only one was expected."""
    pass


class DoesNotExist(Exception):
    """The query returned None objects when only one was expected."""
    pass


class UniqueError(Exception):
    pass


class MongoClientError(Exception):
    pass


class DefaultError(Exception):
    pass