# -*- coding: utf-8 -*-

import importlib


class Settings(dict):
    """Application related settings.

    Load application settings. To set or add extra settings use
    ``Settings.update``.

    :Example:

    >>> settings = Settings('echo.settings')
    >>> # set settings
    >>> settings.update({'SETTINGS_A': 'hello', 'SETTINGS_B': 'world'})
    >>> print(settings['SETTINGS_A'])
    'hello'
    >>> print(settings.get('SETTINGS_C', 'missing'))
    'missing'
    """
    def __init__(self, uri):
        self._uri = uri
        settings = importlib.import_module(self._uri)
        for k in dir(settings):
            if self.is_valid(k):
                self[k] = getattr(settings, k)

    @staticmethod
    def is_valid(name):
        return name.isupper()

    def __repr__(self):
        return '<{} uri={!r}>'.format(self.__class__.__name__, self._uri)
