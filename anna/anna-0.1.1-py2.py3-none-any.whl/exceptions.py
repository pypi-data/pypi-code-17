# -*- coding: utf-8 -*-

from __future__ import unicode_literals


class ConfigurationError(Exception):
    pass


class IncompleteConfigurationError(ConfigurationError):
    def __init__(self, parameter, path):
        super(IncompleteConfigurationError, self).__init__(
            'Configuration does not specify parameter "%s" which should be located at "%s"'
            % (parameter.name, path)
        )


class InvalidPathError(ConfigurationError):
    def __init__(self, path):
        super(InvalidPathError, self).__init__('Path "%s" is unreachable' % path)


class ParameterError(ConfigurationError):
    def __init__(self, msg, parameter=None):
        if parameter is not None:
            super(ParameterError, self).__init__('%s: %s' % (parameter, msg))
        else:
            super(ParameterError, self).__init__(msg)


class InvalidRepresentationError(ParameterError):
    def __init__(self, msg, parameter=None):
        super(InvalidRepresentationError, self).__init__(msg, parameter)


class InvalidUnitError(InvalidRepresentationError):
    def __init__(self, msg, parameter=None):
        super(InvalidUnitError, self).__init__(msg, parameter)
