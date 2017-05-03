# -*- coding: utf-8 -*-
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Pool implementation to manage multiple services at the same time."""

import logging
from threading import Thread


def service_manager(service, connection=None, session=None):
    """Run a service in an infinitive loop until an exception occurs.

    :param service: Selenol service to be executed.
    :param connection: Selenol backend connection.
    :param session: Database session for the service.
    """
    try:
        process = service(connection, session)
        process.run()
    except Exception as ex:
        logging.exception(ex)


class SelenolPool(object):
    """Pool of thread to process services."""

    def __init__(self, services):
        """Constructor.

        :param services: List of services that the pool will manage.
        """
        self.services = services
        self.processess = []

    def serve(self):
        """Create all the services and run them in parallel."""
        self.processess = [Thread(target=service_manager, args=[service]) for
                           service in self.services]
        for process in self.processess:
            process.start()
