# -*- coding: utf-8 -*-
"""
    pip_services_container.info.ContainerInfoFactory
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Container info factory implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .ContainerInfo import ContainerInfo

from pip_services_commons.refer import Descriptor
from pip_services_commons.build import Factory

ContainerInfoFactoryDescriptor = Descriptor(
    "pip-services-container", "factory", "container-info", "default", "1.0"
)

ContainerInfoDescriptor = Descriptor(
    "pip-services-container", "container-info", "default", "default", "1.0"
)

class ContainerInfoFactory(Factory):

    def __init__(self):
        self.register_as_type(ContainerInfoDescriptor, ContainerInfo)
