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

from abc import ABCMeta, abstractmethod
from pluginsmanager.model.updates_observer import UpdatesObserver


class ApplicationObserver(UpdatesObserver, metaclass=ABCMeta):
    """
    The :class:`ApplicationObserver` extends :class:`UpdatesObserver`.
    It is an abstract class definition for treatment of changes in some class model.
    Your methods are called when occurs any change in Bank, Pedalboard, Effect, etc.

    To do this, it is necessary that the :class:`ApplicationObserver` objects
    be registered in some manager, so that it reports the changes. An
    example of a manager is :class:`NotificationController`.

    :class:`NotificationController`, comparing with, :class:`UpdatesObserver`
    add TOKEN. Each observer should have a unique token. This token will differentiate who
    is making requests so the manager does not notify you back.

    For example, if a component requires the manager to have an effect change its
    state (`effect.active = not effect.active`), it is not necessary for the manager
    to inform the component of the change. If the component was informed, it might not know
    that it was the one that requested the change and possibly would update its interface
    erroneously.
    """

    def __init__(self):
        super(ApplicationObserver, self).__init__()

    @property
    @abstractmethod
    def token(self):
        """
        Observer token identifier.
        :return: string for token identifier
                 or None if is not necessary identify the observer
                 (it will receive all notification)
        """
        return None

    @abstractmethod
    def on_current_pedalboard_changed(self, pedalboard, token=None):
        pass
