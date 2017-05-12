# Copyright 2017 SrMouraSilva
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import time
import os
from shutil import copytree
from pathlib import Path

from application.controller.banks_controller import BanksController
from application.controller.current_controller import CurrentController
from application.controller.component_data_controller import ComponentDataController
from application.controller.device_controller import DeviceController
from application.controller.effect_controller import EffectController
from application.controller.notification_controller import NotificationController
from application.controller.param_controller import ParamController
from application.controller.pedalboard_controller import PedalboardController
from application.controller.plugins_controller import PluginsController

from pluginsmanager.mod_host.mod_host import ModHost

from unittest.mock import MagicMock


class Application(object):
    """
    PedalPi - Application is a api for manager the PedalPi - `Components`_
    offers an auto initialization and an updates notification between the components.

    .. _Components: https://github.com/PedalPi/Components

    By a application instance, it's possible obtains a :class:Controller
    for control::

        >>> from application.application import Application
        >>> from application.controller.CurrentController import CurrentController

        >>> application = Application()
        >>> current_controller = application.controller(CurrentController)

        >>> print(current_controller.current_pedalboard)
        <Pedalboard object as Shows with 2 effects at 0x7fa3bcb49be0>

        >>> current_controller.to_next_pedalboard()
        >>> current_controller.current_pedalboard
        <Pedalboard object as Shows 2 with 1 effects at 0x7fa3bbcdecf8>

    For more details see the Controllers extended classes.

    :param string path_data: Path where the data will be persisted
    :param string address: `mod-host`_ address
    :param bool test: If ``test == True``, the connection with mod-host will be simulated

    .. _mod-host: https://github.com/moddevices/mod-host
    """

    def __init__(self, path_data="data/", address="localhost", test=False):
        self.mod_host = self._initialize(address, test)

        self.path_data = self._initialize_data(path_data)
        self.components = []
        self.controllers = self._load_controllers()

        self._configure_controllers(self.controllers)

    def _initialize(self, address, test=False):
        mod_host = ModHost(address)
        if test:
            mod_host.host = MagicMock()
        else:
            mod_host.connect()

        return mod_host

    def _initialize_data(self, path):
        if not os.path.exists(path):
            default_path_data = os.path.dirname(os.path.abspath(__file__)) / Path('data')

            ignore_files = lambda d, files: [f for f in files if (Path(d) / Path(f)).is_file() and f.endswith('.py')]
            copytree(str(default_path_data), str(os.path.abspath(path)), ignore=ignore_files)

            self.log('Data - Create initial data')

        self.log('Data - Loads', os.path.abspath(path))
        return path

    def _teste(self, d, files):
        for f in files:
            print(f)
        return

    def _load_controllers(self):
        controllers = {}

        list_controllers = [
            BanksController,
            ComponentDataController,
            CurrentController,
            DeviceController,
            EffectController,
            NotificationController,
            ParamController,
            PedalboardController,
            PluginsController,
        ]

        for controller in list_controllers:
            controllers[controller.__name__] = controller(self)

        return controllers

    def _configure_controllers(self, controllers):
        for controller in list(controllers.values()):
            controller.configure()
            self.log('Load controller -', controller.__class__.__name__)

    def register(self, component):
        """
        Register a :class:`Component` extended class into Application.
        The components will be loaded when application is loaded (after `start` method is called).

        :param Component component: A module to be loaded when the Application is loaded
        """
        self.components.append(component)

    def start(self):
        """
        Start this API, initializing the components.
        """
        current_pedalboard = self.controller(CurrentController).current_pedalboard
        self.log('Load current pedalboard -', '"' + current_pedalboard.name + '"')
        self.mod_host.pedalboard = current_pedalboard

        for component in self.components:
            component.init()
            self.log('Load component -', component.__class__.__name__)

    def controller(self, controller):
        """
        Returns the controller instance by Controller class identifier

        :param Controller controller: Class identifier
        :return: Controller instance
        """
        return self.controllers[controller.__name__]

    def dao(self, dao):
        """
        Returns a Dao persister instance by Dao class identifier

        :param dao: Class identifier
        :return: Dao instance
        """
        return dao(self.path_data)

    def log(self, *args, **kwargs):
        print('[' + time.strftime('%Y-%m-%d %H:%M:%S') + ']', *args, **kwargs)
