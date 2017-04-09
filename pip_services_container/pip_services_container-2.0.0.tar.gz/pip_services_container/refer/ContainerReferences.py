# -*- coding: utf-8 -*-
"""
    pip_services_container.refer.ContainerReferences
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Container references implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from pip_services_commons.config import IConfigurable
from pip_services_commons.build import CreateException
from pip_services_commons.refer import References
from pip_services_commons.refer import ReferenceException
from pip_services_commons.refer import IReferenceable
from pip_services_commons.reflect import TypeReflector

from ..config.ComponentConfig import ComponentConfig
from ..config.ContainerConfig import ContainerConfig
from .ManagedReferences import ManagedReferences

class ContainerReferences(ManagedReferences):
    
    def __init__(self):
        super(ContainerReferences, self).__init__()

    def put_from_config(self, config):
        for component_config in config:
            component = None
            locator = None

            try:
                # Create component dynamically
                if component_config.type != None:
                    locator = component_config.type
                    component = TypeReflector.create_instance_by_descriptor(component_config.type)
                # Or create component statically
                elif component_config.descriptor != None:
                    locator = component_config.descriptor
                    factory = self._builder.find_factory(locator)
                    component = self._builder.create(locator, factory)
                    if component == None:
                        raise ReferenceException(None, locator)
                    locator = self._builder.clarify_locator(locator, factory)

                # Check that component was created
                if component == None:
                    raise CreateException("CANNOT_CREATE_COMPONENT", "Cannot create component") \
                        .with_details("config", config)

                # Add component to the list
                self._references.put(locator, component)

                # Configure component
                if isinstance(component, IConfigurable):
                    component.configure(component_config.config)

                # Set references to factories
                if isinstance(component, IReferenceable):
                    component.set_references(self)

            except Exception as ex:
                raise ReferenceException(None, locator).with_cause(ex)
