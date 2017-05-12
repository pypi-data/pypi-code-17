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


class NotificationController(Controller):
    """
    Notifies request changes to all :class:`ApplicationObserver` registered
    than not contains the same request _token_.
    """

    def __init__(self, app):
        super().__init__(app)
        self.observers = []

    def configure(self):
        pass

    def register(self, observer):
        """
        Register an observer

        :param ApplicationObserver observer: An observer that will be received the changes
        """
        self.observers.append(observer)

    def unregister(self, observer):
        """
        Unregister an observer
        
        :param ApplicationObserver observer: An observer that not will be more received the changes
        """
        self.observers.remove(observer)

    def is_requester(self, observer, token):
        """
        Verify if the observer is the requester change (if observer contains
        same token that token informed)

        :param ApplicationObserver observer:
        :param string token: Request token identifier
        :return: The requisition is realized by observer?
        """
        return observer.token is not None and observer.token == token

    ########################
    # Notify methods
    ########################
    def current_pedalboard_changed(self, pedalboard, token=None):
        """
        Notify current pedalboard change.

        :param Pedalboard pedalboard: New current pedalboard
        :param string token: Request token identifier
        """
        for observer in self.observers:
            if not self.is_requester(observer, token):
                observer.on_current_pedalboard_changed(pedalboard, token)

    def bank_updated(self, bank, update_type, index, origin, token=None):
        """
        Notify changes in :class:`Bank`.

        :param Bank bank: Bank changed.
        :param UpdateType update_type: Change type
        :param string token: Request token identifier
        :param int index: Bank index (or old index if update_type == UpdateType.DELETED)
        :param BanksManager origin: BanksManager that the bank is (or has) contained
        """
        for observer in self.observers:
            if not self.is_requester(observer, token):
                observer.on_bank_updated(bank, update_type, index=index, origin=origin, token=token)

    def pedalboard_updated(self, pedalboard, update_type, index, origin, token=None):
        """
        Notify changes in :class:`Pedalboard`.

        :param Pedalboard pedalboard: Pedalboard changed
        :param UpdateType update_type: Change type
        :param int index: Pedalboard index (or old index if update_type == UpdateType.DELETED)
        :param Bank origin: Bank that the pedalboard is (or has) contained
        :param string token: Request token identifier
        """
        for observer in self.observers:
            if not self.is_requester(observer, token):
                observer.on_pedalboard_updated(pedalboard, update_type, index=index, origin=origin, token=token)

    def effect_updated(self, effect, update_type, index, origin, token=None):
        """
        Notify changes in :class:`Effect`.

        :param Effect effect: Effect changed
        :param UpdateType update_type: Change type
        :param int index: Effect index (or old index if update_type == UpdateType.DELETED)
        :param Pedalboard origin: Pedalboard that the effect is (or has) contained
        :param string token: Request token identifier
        """
        for observer in self.observers:
            if not self.is_requester(observer, token):
                observer.on_effect_updated(effect, update_type, index=index, origin=origin, token=token)

    def effect_status_toggled(self, effect, token=None):
        """
        Notify :class:`Effect` status toggled.

        :param Effect effect: Effect when status has been toggled
        :param string token: Request token identifier
        """
        for observer in self.observers:
            if not self.is_requester(observer, token):
                observer.on_effect_status_toggled(effect, token)

    def param_value_changed(self, param, token=None, **kwargs):
        """
        Notify :class:`Param` value change.

        :param Param param: Param with value changed
        :param string token: Request token identifier
        """
        for observer in self.observers:
            if not self.is_requester(observer, token):
                observer.on_param_value_changed(param, token, **kwargs)

    def connection_updated(self, connection, update_type, pedalboard, token=None):
        """
        Notify :class:`Connection` addictions and removals.

        :param Connection connection: Connection added or removed
        :param UpdateType update_type: Change type
        :param Pedalboard pedalboard: Pedalboard that the connection is (or has) contained
        :param string token: Request token identifier
        """
        for observer in self.observers:
            if not self.is_requester(observer, token):
                observer.on_connection_updated(connection, update_type, pedalboard=pedalboard, token=token)
