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
from application.controller.current_controller import CurrentController
from application.controller.notification_controller import NotificationController

from pluginsmanager.model.update_type import UpdateType


class PedalboardError(Exception):
    pass


class PedalboardController(Controller):
    """
    Manage :class:`Pedalboard`, informing the creation, informing the updates
    or deleting and informing it.
    """

    def __init__(self, application):
        super(PedalboardController, self).__init__(application)
        self.dao = None
        self.banks = None
        self.current = None
        self.notifier = None

    def configure(self):
        self.dao = self.app.dao(BankDao)
        self.banks = self.app.controller(BanksController)
        self.current = self.app.controller(CurrentController)
        self.notifier = self.app.controller(NotificationController)

    def created(self, pedalboard, token=None):
        """
        Notify all observers that the :class:`Pedalboard` object has been created.

        .. note::

            The pedalboard needs be added in a :class:`Bank` before.

            >>> bank.append(pedalboard)
            >>> pedalboard_controller.created(pedalboard)

        :param Pedalboard pedalboard: Pedalboard created
        :param string token: Request token identifier
        """
        if pedalboard.bank not in self.banks.banks:
            raise PedalboardError('Bank of pedalboard {} not added in banks manager'.format(pedalboard))

        self._save(pedalboard)
        self._notify_change(pedalboard, UpdateType.CREATED, token)

    def update(self, pedalboard, token=None, reload=True):
        """
        Notify all observers that the :class:`Pedalboard` object has updated
        and persists the new state.

        .. note::
            If you're changing the current pedalboard, the pedalboard should be
            fully charged and loaded. So, prefer the use of other Controllers
            methods for simple changes.

        :param Pedalboard pedalboard: Pedalboard to be updated
        :param string token: Request token identifier
        :param bool reload: If it's the current pedalboard, is necessary reload the plugins?
        """
        if pedalboard.bank not in self.banks.banks:
            raise PedalboardError('Bank of pedalboard {} not added in banks manager'.format(pedalboard))

        self._save(pedalboard)

        if self.current.is_current_pedalboard(pedalboard) and reload:
            self.current.reload_current_pedalboard()

        self._notify_change(pedalboard, UpdateType.UPDATED, token)

    def replace(self, old_pedalboard, new_pedalboard, token=None):
        """
        Replaces the old pedalboard to new pedalboard and notifies all observers that the
        :class:`Pedalboard` object has UPDATED

        .. note::
            If you're changing a bank that has a current pedalboard,
            the pedalboard should be fully charged and loaded. So, prefer the use
            of other Controllers methods for simple changes.

        :param Pedalboard old_pedalboard: Pedalboard that will be replaced for new_pedalboard
        :param Pedalboard new_pedalboard: Pedalboard that replaces old_pedalboard
        :param string token: Request token identifier
        """
        if old_pedalboard.bank not in self.banks.banks:
            raise PedalboardError('Bank of old_pedalboard {} not added in banks manager'.format(old_pedalboard))

        if new_pedalboard.bank is not None:
            raise PedalboardError('Bank of new_pedalboard {} already added in banks manager'.format(new_pedalboard))

        bank = old_pedalboard.bank
        bank.pedalboards[bank.pedalboards.index(old_pedalboard)] = new_pedalboard
        self.update(new_pedalboard, token)

    def delete(self, pedalboard, token=None):
        """
        Remove the :class:`Pedalboard` of your bank.

        .. note::
            If the pedalboard is the current, another pedalboard will be loaded
            and it will be the new current pedalboard.

        :param Pedalboard pedalboard: Pedalboard to be removed
        :param string token: Request token identifier
        """
        if pedalboard.bank not in self.banks.banks:
            raise PedalboardError('Bank of pedalboard {} not added in banks manager'.format(pedalboard))

        # Get next pedalboard if the removed is the current pedalboard
        next_pedalboard = None
        if self.current.is_current_pedalboard(pedalboard):
            self.current.to_next_pedalboard()
            next_pedalboard = self.current.current_pedalboard

        bank = pedalboard.bank

        # Remove
        pedalboard_index = pedalboard.index
        del pedalboard.bank.pedalboards[pedalboard_index]
        self._notify_change(pedalboard, UpdateType.DELETED, token, index=pedalboard_index, origin=bank)

        # Update current pedalboard
        #only_pedalboard_bank_has_removed = len(bank.pedalboards) == 0
        #if only_pedalboard_bank_has_removed:
        #    self.current.remove_current(token=token)

        #elif next_pedalboard is not None:
        if next_pedalboard is not None:
            self.current.pedalboard_number = next_pedalboard.index

        self.dao.save(bank, self.banks.banks.index(bank))

    def move(self, pedalboard, new_position, token=None):
        """
        Move the pedalboard from the current position in your bank.pedalboards list for the new position::

            >>> # Move the last pedalboard for second position
            >>> bank.pedalboards
            [pedalboard a, pedalboard b, pedalboard c, pedalboard d]
            >>> pedalboard_d = bank.pedalboards[-1]
            >>> pedalboard_d
            pedalboard_d
            >>> pedalboard_controller.move(pedalboard_d, 1)
            >>> bank.pedalboards
            [pedalboard a, pedalboard d, pedalboard b, pedalboard c]

        :param Pedalboard pedalboard: Pedalboard that will be the position in your bank changed
        :param int new_position: New index position of the pedalboard
        :param string token: Request token identifier
        """
        current_pedalboard = self.current.current_pedalboard

        pedalboards = pedalboard.bank.pedalboards
        pedalboards.insert(new_position, pedalboards.pop(pedalboard.index))

        self._notify_change(pedalboard, UpdateType.UPDATED, token=token)
        self._save(pedalboard)

        # Save the current pedalboard data
        # The current pedalboard index changes then changes the pedalboard order
        if current_pedalboard.bank == pedalboard.bank:
            self.current._set_current(current_pedalboard, notify=False)

    def _save(self, pedalboard):
        bank = pedalboard.bank
        self.dao.save(bank, self.banks.banks.index(bank))

    def _notify_change(self, pedalboard, update_type, token=None, **kwargs):
        index = kwargs.pop('index') if 'index' in kwargs else pedalboard.index
        origin = kwargs.pop('origin') if 'origin' in kwargs else pedalboard.bank

        self.notifier.pedalboard_updated(pedalboard, update_type, index=index, origin=origin, token=token, **kwargs)
