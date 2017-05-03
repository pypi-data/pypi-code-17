# -*- coding: utf-8 -*-
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Params declarations."""

from .exceptions import SelenolInvalidArgumentException


def selenol_params(**kwargs):
    """Decorate request parameters to transform them into Selenol objects."""
    def params_decorator(func):
        """Param decorator.

        :param f: Function to decorate, typically on_request.
        """
        def service_function_wrapper(service, message):
            """Wrap function call.

            :param service: SelenolService object.
            :param message: SelenolMessage request.
            """
            params = {k: f(service, message) for k, f in kwargs.items()}
            return func(service, **params)
        return service_function_wrapper
    return params_decorator


def _get_value(data_structure, key):
    """Return the value of a data_structure given a path.

    :param data_structure: Dictionary, list or subscriptable object.
    :param key: Array with the defined path ordered.
    """
    if len(key) == 0:
        raise KeyError()
    value = data_structure[key[0]]
    if len(key) > 1:
        return _get_value(value, key[1:])
    return value


def get_value_from_session(key):
    """Get a session value from the path specifed.

    :param key: Array that defines the path of the value inside the message.
    """
    def value_from_session_function(service, message):
        """Actual implementation of get_value_from_session function.

        :param service: SelenolService object.
        :param message: SelenolMessage request.
        """
        return _get_value(message.session, key)
    return value_from_session_function


def get_value_from_content(key):
    """Get a value from the path specifed.

    :param key: Array that defines the path of the value inside the message.
    """
    def value_from_content_function(service, message):
        """Actual implementation of get_value_from_content function.

        :param service: SelenolService object.
        :param message: SelenolMessage request.
        """
        return _get_value(message.content, key)
    return value_from_content_function


def get_object_from_content(entity, key):
    """Get an object from the database given an entity and the content key.

    :param entity: Class type of the object to retrieve.
    :param key: Array that defines the path of the value inside the message.
    """
    def object_from_content_function(service, message):
        """Actual implementation of get_object_from_content function.

        :param service: SelenolService object.
        :param message: SelenolMessage request.
        """
        id_ = get_value_from_content(key)(service, message)
        result = service.session.query(entity).get(id_)
        if not result:
            raise SelenolInvalidArgumentException(key, id_)
        return result
    return object_from_content_function


def get_object_from_session(entity, key):
    """Get an object from the database given an entity and the session key.

    :param entity: Class type of the object to retrieve.
    :param key: Array that defines the path of the value inside the message.
    """
    def object_from_session_function(service, message):
        """Actual implementation of get_object_from_session function.

        :param service: SelenolService object.
        :param message: SelenolMessage request.
        """
        id_ = get_value_from_session(key)(service, message)
        result = service.session.query(entity).get(id_)
        if not result:
            raise SelenolInvalidArgumentException(key, id_)
        return result
    return object_from_session_function


def get_request_id():
    """Get the request ID specified in the message."""
    def request_id_function(service, message):
        """Actual implementation of get_request_id function.

        :param service: SelenolService object.
        :param message: SelenolMessage request.
        """
        return message.request_id
    return request_id_function
