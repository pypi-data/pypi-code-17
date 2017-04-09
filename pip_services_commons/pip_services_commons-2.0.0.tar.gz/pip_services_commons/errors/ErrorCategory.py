# -*- coding: utf-8 -*-
"""
    pip_services_commons.errors.ErrorCategory
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Error categories enumeration
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class ErrorCategory(object):
    """
    Defines broad categories of application errors.
    """

    Unknown = 'Unknown'
    """
    Unknown or unexpected errors
    """

    Internal = 'Internal'
    """
    Internal errors caused by programming mistakes
    """

    Misconfiguration = 'Misconfiguration'
    """
    Errors related to mistakes in user-defined configuration
    """

    InvalidState = 'InvalidState'
    """
    Errors related to operations called in wrong component state.
    For instance, business calls when component is not ready
    """

    NoResponse = 'NoResponse'
    """
    Errors happened during connection to remote services.
    They can be related to misconfiguration, network issues
    or remote service itself 
    """

    FailedInvocation = 'FailedInvocation'
    """
    Errors returned by remote services or network
    during call attempts
    """

    FileError = 'FileError'
    """
    Errors in read/write file operations
    """

    BadRequest = 'BadRequest'
    """
    Errors due to improper user requests, like
    missing or wrong parameters 
    """

    Unauthorized = 'Unauthorized'
    """
    Access errors caused by missing user identity
    or security permissions
    """

    NotFound = 'NotFound'
    """
    Error caused by attempt to access missing object
    """

    Conflict = 'Conflict'
    """
    Errors raised by conflict in object versions
    posted by user and stored on server.
    """

    Unsupported = 'Unsupported'
    """
    Errors caused by calls to unsupported
    or not yet implemented functionality
    """
