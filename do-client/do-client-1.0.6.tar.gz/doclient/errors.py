#! coding=utf-8
"""DigitalOcean APIv2 client errors module"""
__author__ = "Sriram Velamur<sriram.velamur@gmail.com>"
__all__ = ("APIAuthError", "InvalidArgumentError",
           "APIError", "NetworkError")

import sys
sys.dont_write_bytecode = True


class BaseError(BaseException):

    """
    DigitalOcean APIv2 base error class.
    Derived error classes need to specify their error message prefix.
    If a child class fails to provide a prefix property,
    prefix defaults to DOClient::GeneralError
    """

    def __init__(self, *args, **kwargs):
        if not args:
            raise RuntimeError("Invalid invocation")
        message = args[0]
        prefix = getattr(self, "prefix", "GeneralError")
        message = "DOClient::{0} {1}: ".format(prefix, message)
        args = (message,)
        super(BaseError, self).__init__(*args, **kwargs)


class APIAuthError(BaseError):
    """
    DigitalOcean APIv2 authentication error class.
    Raised when client initialization receives a HTTP 401 while
    requesting for list of instances associated with the account.
    """

    prefix = "APIAuthError"


class InvalidArgumentError(BaseError):
    """
    DigitalOcean APIv2 method arugment error class.
    Raised when a method receives an invalid, empty,
    or type mismatching value for an arugment.
    """

    prefix = "InvalidArgumentError"


class APIError(BaseError):
    """
    DigitalOcean APIv2 generic API error class.
    Raised when a failure response is received from the
    API that is not an authentication related one.
    """

    prefix = "APIError"


class NetworkError(BaseError):
    """
    DigitalOcean APIv2 client fallback network error class.
    Raised when requests library encounters a network error
    while attempting to contact the DigitalOcean API.
    """

    prefix = "NetworkError"
