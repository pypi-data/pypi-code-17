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

from pluginsmanager.model.update_type import UpdateType


class EffectController(Controller):
    """
    Manage :class:`Effect`, creating new, deleting or changing status.
    """

    def __init__(self, application):
        super(EffectController, self).__init__(application)
        self.dao = None
        self.banks = None
        self.current = None
        self.device = None
        self.notifier = None

    def configure(self):
        from application.controller.current_controller import CurrentController
        self.dao = self.app.dao(BankDao)
        self.banks = self.app.controller(BanksController)
        self.current = self.app.controller(CurrentController)
        self.device = self.app.controller(DeviceController)
        self.notifier = self.app.controller(NotificationController)

    def created(self, effect, token=None):
        """
        Persists the :class:`Effect` object created in your :class:`Pedalboard`

        .. note::

            The effect needs be added in a :class:`Pedalboard` before.

            >>> pedalboard.add(effect)
            >>> effect_controller.created(effect)

        :param Effect effect: Effect created and added in your Pedalboard
        :param string token: Request token identifier
        """
        self._save(effect.pedalboard)
        self._notify_change(effect, UpdateType.CREATED, token)

    def delete(self, effect, token=None):
        """
        Remove an :class:`Effect` instance in your :class:`Pedalboard`

        :param Effect effect: Effect will be removed
        :param string token: Request token identifier
        """
        pedalboard = effect.pedalboard

        self._notify_change(effect, UpdateType.DELETED, token)
        pedalboard.effects.remove(effect)

        self._save(pedalboard)

    def toggle_status(self, effect, token=None):
        """
        Toggle the effect status: ``status = not effect.status`` and
        notifies the change

        :param Effect effect: Effect will be toggled your status
        :param string token: Request token identifier
        """
        effect.toggle()

        self._save(effect.pedalboard)
        self.notifier.effect_status_toggled(effect, token)

    def _notify_change(self, effect, update_type, token, **kwargs):
        index = kwargs.pop('index', effect.index)
        origin = kwargs.pop('origin', effect.pedalboard)

        self.notifier.effect_updated(effect, update_type, index=index, origin=origin, token=token, **kwargs)

    def connected(self, pedalboard, connection, token=None):
        """
        Informs the :class:`Connection` object has ben created

        :param Pedalboard pedalboard: Pedalboard where has added the connection
        :param Connection connection: Connection created
        :param string token: Request token identifier
        """
        self._save(pedalboard)

        self.notifier.connection_updated(connection, UpdateType.CREATED, pedalboard=pedalboard, token=token)

    def disconnected(self, pedalboard, connection, token=None):
        """
        Informs the :class:`Connection` object has ben removed

        :param Pedalboard pedalboard: Pedalboard where has removed the connection
        :param Connection connection: Connection removed
        :param string token: Request token identifier
        """
        self._save(pedalboard)

        self.notifier.connection_updated(connection, UpdateType.DELETED, pedalboard=pedalboard, token=token)

    def _save(self, pedalboard):
        bank = pedalboard.bank
        index = self.banks.banks.index(bank)
        self.dao.save(bank, index)
