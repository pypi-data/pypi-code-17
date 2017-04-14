"""
Copyright (C) 2014-2017 cloudover.io ltd.
This file is part of the CloudOver.org project

Licensee holding a valid commercial license for this software may
use it in accordance with the terms of the license agreement
between cloudover.io ltd. and the licensee.

Alternatively you may use this software under following terms of
GNU Affero GPL v3 license:

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version. For details contact
with the cloudover.io company: https://cloudover.io/


This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.


You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from corenetwork.exceptions.config import *
import importlib
import imp
import sys

settings = None
try:
    from corecluster import settings
except:
    pass

try:
    from corenode import settings
except:
    pass


def get(config, variable, default=None):
    if settings is None:
        raise ConfigSyntaxError('settings_not_loaded')

    for app_name in settings.APPS:
        app = importlib.import_module(app_name).MODULE
        if 'configs' in app and config in app['configs']:
            try:
                sys.dont_write_bytecode = True
                config_content = imp.load_source(config, app['configs'][config])
            except Exception as e:
                raise ConfigSyntaxError(str(e))

            if hasattr(config_content, variable):
                return getattr(config_content, variable)
            elif default is not None:
                return default
            else:
                raise ConfigVariableNotFound(variable)

    # In case when loop iterated over all configs
    raise ConfigVariableNotFound('config ' + config)


def get_algorithm(name):
    for app_name in settings.APPS:
        app = importlib.import_module(app_name).MODULE
        if 'algorithms' in app:
            if name in app['algorithms']:
                return importlib.import_module(app['algorithms'][name])
    raise ConfigVariableNotFound('ALGORITHM: ' + name)