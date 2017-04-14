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

import importlib

class HookInterface(object):
    '''
    This class delivers interface for node hooks. This may be used to trigger several actions executed on
    virtual machine, node or network.
    '''
    actions = []

    def start(self):
        """
        Override this method in hook's code to perform additional actions on action prepare (e.g. hook, networking or vm)
        """
        pass


    def finish(self):
        """
        Override this method in hook's code to perform additional actions on action finish (e.g. hook, networking or vm)
        """
        pass


    def failed(self):
        """
        Override this method in hook's core to handle failure of action. This is called instead finish method on any
        exception raised after hooks' start.
        """

    def cron(self, interval):
        """
        Override this method in hook's code to perform periodic actions on object (e.g. vm, image or network) in periodic
        time. This may be used to monitor vm's state.
        :param interval The frequency of hook calling. You could
        """
        pass


    @staticmethod
    def get_hooks(action, pipeline='node'):
        '''
        Get list with Hook
        :param action: Name of action which is triggering hook call
        :param pipeline: Deprecated.
        :return:
        '''
        hook_scripts = []
        from corenetwork.utils.config import settings
        from corenetwork.utils.logger import log

        for app_name in settings.APPS:
            app = importlib.import_module(app_name).MODULE
            if 'hooks' in app and action in app['hooks']:
                hook_scripts.extend(app['hooks'][action])

        hooks = []

        for hook in hook_scripts:
            try:
                hooks.append(importlib.import_module(hook).Hook())
            except Exception as e:
                log(msg='Failed to import hook: %s' % hook, exception=e, tags=('hook', 'fatal', 'error'))

        return hooks
