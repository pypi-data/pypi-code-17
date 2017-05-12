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

from application.dao.bank_dao import BankDao

from application.controller.controller import Controller
from application.controller.banks_controller import BanksController
from application.controller.device_controller import DeviceController
from application.controller.notification_controller import NotificationController


class ParamError(Exception):
    pass


class ParamController(Controller):
    """
    Manage :class:`Param`, updating your value
    """

    def __init__(self, application):
        super(ParamController, self).__init__(application)
        self.dao = None
        self.banks = None
        self.device = None
        self.notifier = None

    def configure(self):
        self.dao = self.app.dao(BankDao)
        self.banks = self.app.controller(BanksController)
        self.device = self.app.controller(DeviceController)
        self.notifier = self.app.controller(NotificationController)

    def updated(self, param, token=None):
        """
        Informs the :class:`Param` are updated.

        .. note::

            Change the param value before to notify

            >>> param.value = new_value
            >>> param_controller.updated(param)

        :param Param param: Effect parameter with your value changed
        :param string token: Request token identifier
        """
        pedalboard = param.effect.pedalboard
        bank = pedalboard.bank

        if bank not in self.banks.banks:
            raise ParamError('Bank of pedalboard {} not added in banks manager'.format(pedalboard))

        self.dao.save(bank, self.banks.banks.index(bank))

        self.notifier.param_value_changed(param, token)
