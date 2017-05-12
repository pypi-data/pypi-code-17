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
from application.controller.device_controller import DeviceController
from application.controller.notification_controller import NotificationController

from application.dao.bank_dao import BankDao

from pluginsmanager.banks_manager import BanksManager
from pluginsmanager.model.bank import Bank
from pluginsmanager.model.update_type import UpdateType


class BankError(Exception):
    pass


class BanksController(Controller):
    """
    Manage :class:`Bank`, creating new, updating or deleting.
    """

    def __init__(self, application):
        super(BanksController, self).__init__(application)

        self.dao = self.app.dao(BankDao)

        self.manager = BanksManager()
        self.current = None
        self.notifier = None

    def configure(self):
        # To fix Cyclic dependence
        from application.controller.current_controller import CurrentController
        self.current = self.app.controller(CurrentController)

        self.notifier = self.app.controller(NotificationController)

        for bank in self.dao.banks(DeviceController.sys_effect):
            bank.original_name = bank.name
            self.manager.append(bank)

    @property
    def banks(self):
        return self.manager.banks

    def create(self, bank, token=None):
        """
        Persists a new :class:`Bank` in database.

        :param Bank bank: Bank that will be added
        :param string token: Request token identifier

        :return int: Bank index
        """
        if bank in self.manager.banks:
            raise BankError('Bank {} already added in banks manager'.format(bank))

        self.manager.append(bank)

        index = len(self.banks) - 1
        self._notify_change(bank, UpdateType.CREATED, token, index=index)

        bank.original_name = bank.name
        self.dao.save(bank, index)

        return index

    def update(self, bank, token=None):
        """
        Notify all observers that the :class:`Bank` object has updated
        and persists the new state.

        .. note::
            If you needs change the bank to other, use ``replace`` instead.

        .. note::
            If you're changing a bank that has a current pedalboard,
            the pedalboard should be fully charged and loaded. So, prefer the use
            of other Controllers methods for simple changes.

        :param Bank bank: Bank updated
        :param string token: Request token identifier
        """
        if bank not in self.manager.banks:
            raise BankError('Bank {} not added in banks manager'.format(bank))

        if bank.name != bank.original_name:
            self.dao.delete(bank)
            bank.original_name = bank.name

        self.dao.save(bank, self.banks.index(bank))

        if self.current.is_current_bank(bank):
            self.current.reload_current_pedalboard()

        self._notify_change(bank, UpdateType.UPDATED, token)

    def replace(self, old_bank, new_bank, token=None):
        """
        Replaces the old bank to new bank and notifies all observers that the
        :class:`Bank` object has UPDATED

        .. note::
            If you're changing a bank that has a current pedalboard,
            the pedalboard should be fully charged and loaded. So, prefer the use
            of other Controllers methods for simple changes.

        :param Bank old_bank: Bank that will be replaced for new_bank
        :param Bank new_bank: Bank that replaces old_bank
        :param string token: Request token identifier
        """
        if old_bank not in self.banks:
            raise BankError('Old bank {} not added in banks manager'.format(old_bank))

        if new_bank in self.banks:
            raise BankError('New bank {} already added in banks manager'.format(new_bank))

        new_bank.original_name = new_bank.name

        index = self.banks.index(old_bank)

        self.dao.delete(old_bank)
        self.dao.save(new_bank, index)

        is_current_bank = self.current.is_current_bank(old_bank)

        self.banks[old_bank.index] = new_bank

        if is_current_bank:
            self.current.reload_current_pedalboard()

        self._notify_change(new_bank, UpdateType.UPDATED, token)

    def delete(self, bank, token=None):
        """
        Remove the informed :class:`Bank`.

        .. note::
            If the Bank contains deleted contains the current pedalboard,
            another pedalboard will be loaded and it will be the new current pedalboard.

        :param Bank bank: Bank to be removed
        :param string token: Request token identifier
        """
        if bank not in self.banks:
            raise BankError('Bank {} not added in banks manager'.format(bank))

        next_bank = None
        if bank == self.current.current_bank:
            self.current.to_next_bank()
            next_bank = self.current.current_bank

        manager = bank.manager
        index = self.banks.index(bank)
        self.dao.delete(bank)
        self.manager.banks.remove(bank)

        if next_bank is not None:
            self.current.bank_number = self.banks.index(next_bank)

        self._notify_change(bank, UpdateType.DELETED, token, index=index, manager=manager)

    def swap(self, bank_a, bank_b, token=None):
        """
        Swap bank_a with bank_b. The bank a position will be the bank b position
        and the bank b position will be the bank a position.

        .. note::
            If the any of the banks contains the current pedalboard
            it will not changed.

        :param Bank bank_a: Bank to the swapped with bank_b
        :param Bank bank_b: Bank to the swapped with bank_a
        :param string token: Request token identifier
        """
        if bank_a not in self.banks:
            raise BankError('Bank {} not added in banks manager'.format(bank_a))
        if bank_b not in self.banks:
            raise BankError('Bank {} not added in banks manager'.format(bank_b))

        index_a = self.banks.index(bank_a)
        index_b = self.banks.index(bank_b)

        current_bank_index = None
        if self.current.is_current_bank(bank_a):
            current_bank_index = index_b
        elif self.current.is_current_bank(bank_b):
            current_bank_index = index_a

        self.banks[index_a], self.banks[index_b] = self.banks[index_b], self.banks[index_a]

        self.dao.save(bank_a, index_b)
        self.dao.save(bank_b, index_a)

        if current_bank_index is not None:
            self.current.bank_number = current_bank_index

        self._notify_change(bank_a, UpdateType.UPDATED, token)
        self._notify_change(bank_b, UpdateType.UPDATED, token)

    def _notify_change(self, bank, update_type, token=None, index=None, manager=None):
        manager = manager if manager is not None else bank.manager
        index = index if index is not None else bank.index

        self.notifier.bank_updated(bank, update_type, index=index, origin=manager, token=token)
