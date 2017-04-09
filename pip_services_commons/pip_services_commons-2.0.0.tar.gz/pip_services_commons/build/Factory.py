# -*- coding: utf-8 -*-
"""
    pip_services_common.build.Factory
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Factory implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .IFactory import IFactory
from .CreateException import CreateException

class Registration:
    def __init__(self, locator, factory):
        self.locator = locator
        self.factory = factory

    locator = None
    factory = None


class Factory(object, IFactory):
    _registrations = []

    def register(self, locator, factory):
        if locator == None:
            raise Exception("Locator cannot be null")
        if factory == None:
            raise Exception("Factory cannot be null")

        self._registrations.append(Registration(locator, factory))

    def register_as_type(self, locator, object_factory):
        if locator == None:
            raise Exception("Locator cannot be null")
        if object_factory == None:
            raise Exception("Factory cannot be null")

        def factory(locator):
            return object_factory()

        self._registrations.append(Registration(locator, factory))

    def can_create(self, locator):
        for registration in self._registrations:
            this_locator = registration.locator
            if this_locator == locator:
                return this_locator
        return None

    def create(self, locator):
        for registration in self._registrations:
            this_locator = registration.locator

            if this_locator == locator:
                try:
                    return registration.factory(locator)
                except Exception as ex:
                    if isinstance(ex, CreateException):
                        raise ex
                    
                    raise CreateException(
                        None,
                        "Failed to create object for " + str(locator)
                    ).with_cause(ex)
