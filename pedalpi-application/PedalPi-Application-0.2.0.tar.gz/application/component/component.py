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

from application.controller.notification_controller import NotificationController


class Component(metaclass=ABCMeta):

    def __init__(self, application):
        self.application = application

    @abstractmethod
    def init(self):
        """
        Initialize this component
        """
        pass

    def controller(self, controller):
        return self.application.controller(controller)

    def register_observer(self, observer):
        """
        Register an observer in :class:`Application` by :class:`NotificationController`.
        Observers will be notified of the changes requested in the application API.

        Obs: If a observer contains a _token_ and the request informs the same _token_
        the observer not will be notified.

        :param UpdatesObserver observer:
        """
        self.controller(NotificationController).register(observer)

    def unregister_observer(self, observer):
        """
        Unregister an observer in :class:`Application` by :class:`NotificationController`.
        The observer not will be more notified of the changes requested in the application API.

        :param UpdatesObserver observer:
        """
        self.controller(NotificationController).unregister(observer)
