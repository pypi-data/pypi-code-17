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

from application.controller.controller import Controller
from application.controller.banks_controller import BanksController
from application.controller.device_controller import DeviceController
from application.controller.effect_controller import EffectController
from application.controller.notification_controller import NotificationController
from application.controller.param_controller import ParamController

from application.dao.current_dao import CurrentDao


class CurrentController(Controller):
    """
    Manage the current :class:`Bank` and current :class:`Pedalboard`
    """

    def __init__(self, application):
        super(CurrentController, self).__init__(application)
        self.dao = None
        self.bank_number = 0
        self.pedalboard_number = 0

        self.device_controller = None
        self.banks_controller = None
        self.effect_controller = None
        self.notifier = None
        self.param_controller = None

    def configure(self):
        self.device_controller = self.app.controller(DeviceController)
        self.banks_controller = self.app.controller(BanksController)
        self.effect_controller = self.app.controller(EffectController)
        self.notifier = self.app.controller(NotificationController)
        self.param_controller = self.app.controller(ParamController)

        self.dao = self.app.dao(CurrentDao)
        data = self.dao.load()
        self.bank_number = data["bank"]
        self.pedalboard_number = data["pedalboard"]

    # ************************
    # Property
    # ************************

    @property
    def current_pedalboard(self):
        """
        Get the current :class:`Pedalboard`
        """
        return self.current_bank.pedalboards[self.pedalboard_number]

    @property
    def current_bank(self):
        """
        Get the :class:`Bank` that contains the current :class:`Pedalboard`
        """
        return self.banks_controller.banks[self.bank_number]

    # ************************
    # Persistance
    # ************************
    def _save_current(self):
        self.dao.save(self.bank_number, self.pedalboard_number)

    # ************************
    # Get of Current
    # ************************
    def is_current_bank(self, bank):
        """
        :param Bank bank:
        :return bool: The :class:`Bank` is the current bank?
        """
        return bank == self.current_bank

    def is_current_pedalboard(self, pedalboard):
        """
        :param Pedalboard pedalboard:
        :return bool: The :class:`Pedalboard` is the current pedalboard?
        """
        return self.is_current_bank(pedalboard.bank) and self.current_pedalboard == pedalboard

    # ************************
    # Set Current Pedalboard/Bank
    # ************************
    def to_before_pedalboard(self, token=None):
        """
        Change the current :class:`Pedalboard` for the previous pedalboard.

        If the current pedalboard is the first in the current :class:`Bank`,
        the current pedalboard is will be the **last of the current Bank**.

        :param string token: Request token identifier
        """
        before_pedalboard_number = self.pedalboard_number - 1
        if before_pedalboard_number == -1:
            before_pedalboard_number = len(self.current_bank.pedalboards) - 1

        self.set_pedalboard(self.current_bank.pedalboards[before_pedalboard_number], token)

    def to_next_pedalboard(self, token=None):
        """
        Change the current :class:`Pedalboard` for the next pedalboard.

        If the current pedalboard is the last in the current :class:`Bank`,
        the current pedalboard is will be the **first of the current Bank**

        :param string token: Request token identifier
        """
        next_pedalboard_number = self.pedalboard_number + 1
        if next_pedalboard_number == len(self.current_bank.pedalboards):
            next_pedalboard_number = 0

        self.set_pedalboard(self.current_bank.pedalboards[next_pedalboard_number], token)

    def set_pedalboard(self, pedalboard, token=None):
        """
        Set the current :class:`Pedalboard` for the pedalboard
        only if the ``pedalboard != current_pedalboard``

        :param Pedalboard pedalboard: New current pedalboard
        :param string token: Request token identifier
        """
        if self.is_current_pedalboard(pedalboard):
            return

        self._set_current(pedalboard, token=token)

    def reload_current_pedalboard(self):
        self._load_device_pedalboard(self.current_pedalboard)

    def to_before_bank(self, token=None):
        """
        Change the current :class:`Bank` for the before bank. If the current
        bank is the first, the current bank is will be the last bank.

        The current pedalboard will be the first of the new current bank.

        :param string token: Request token identifier
        """
        banks = self.banks_controller.banks
        position = self.bank_number

        before_index = position - 1
        if before_index == -1:
            before_index = len(banks) - 1

        self.set_bank(banks[before_index], token=token)

    def to_next_bank(self, token=None):
        """
        Change the current :class:`Bank` for the next bank. If the current
        bank is the last, the current bank is will be the first bank.

        The current pedalboard will be the first of the new current bank.

        :param string token: Request token identifier
        """
        banks = self.banks_controller.banks
        position = self.bank_number

        next_index = position + 1
        if next_index == len(banks):
            next_index = 0

        self.set_bank(banks[next_index], token=token)

    def set_bank(self, bank, token=None, notify=True):
        """
        Set the current :class:`Bank` for the bank
        only if the ``bank != current_bank``

        :param Bank bank: Bank that will be the current
        :param string token: Request token identifier
        :param bool notify: If false, not notify change for :class:`UpdatesObserver`
                            instances registered in :class:`Application`
        """
        if self.current_bank == bank:
            return

        self._set_current(bank.pedalboards[0], token, notify)

    def _set_current(self, pedalboard, token=None, notify=True):
        self._load_device_pedalboard(pedalboard)  # throwable. need be first

        bank_number = self.banks_controller.banks.index(pedalboard.bank)
        pedalboard_number = pedalboard.index

        self.bank_number = bank_number
        self.pedalboard_number = pedalboard_number

        self._save_current()

        if notify:
            self.notifier.current_pedalboard_changed(self.current_pedalboard, token)

    def _load_device_pedalboard(self, pedalboard):
        self.device_controller.pedalboard = pedalboard

    '''
    def remove_current(self, token=None):
        """
        That not exists any pedalboard running
        :param string token: Request token identifier
        """
        self.device_controller.pedalboard = None
        self.bank_number = None
        self.pedalboard_number = None

        self._save_current()

        self.notifier.current_pedalboard_changed(self.current_pedalboard, token)
    '''