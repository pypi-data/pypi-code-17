# -*- coding: utf-8 -*-

#    Virtual-IPM is a software for simulating IPMs and other related devices.
#    Copyright (C) 2017  The IPMSim collaboration <http://ipmsim.gitlab.io/IPMSim>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import, unicode_literals

import injector

from virtual_ipm.components import Manager
import virtual_ipm.di as di
from virtual_ipm.timings import measure_cpu_time


class DeviceManager(Manager):
    """
    This component provides functionality for checking if particles are to be detected or if
    they reached an invalid situation.
    """

    @injector.inject(
        device=di.models.device,
        particle_supervisor=di.components.particle_supervisor
    )
    def __init__(self, device, particle_supervisor):
        super(DeviceManager, self).__init__()
        self._device = device
        self._particle_supervisor = particle_supervisor
        self._lower_boundaries = self._device.lower_boundaries
        self._upper_boundaries = self._device.upper_boundaries

    def as_json(self):
        return dict(
            super(DeviceManager, self).as_json(),
            model=self._device.as_json()
        )

    @measure_cpu_time
    def prepare(self):
        """
        Prepare the device model.
        """
        super(DeviceManager, self).prepare()
        self._device.prepare()

    @measure_cpu_time
    def scan_particles(self, progress):
        """
        Scan all particles that are currently being tracked and update their statuses if necessary.
        This is achieved by invoking the model's :method:`DeviceModel.scan_particles` method.

        Parameters
        ----------
        progress : :class:`Progress`
        """
        tracked_particles = self._particle_supervisor.tracked_particles
        if tracked_particles:
            self._device.scan_particles(tracked_particles, progress)

    @property
    def x_min(self):
        """
        Retrieve the lower boundary in x-direction.

        Returns
        -------
        x_min : float
            In units of [m].
        """
        return self._lower_boundaries[0]

    @property
    def x_max(self):
        """
        Retrieve the upper boundary in x-direction.

        Returns
        -------
        x_max : float
            In units of [m].
        """
        return self._upper_boundaries[0]

    @property
    def y_min(self):
        """
        Retrieve the lower boundary in y-direction.

        Returns
        -------
        y_min : float
            In units of [m].
        """
        return self._lower_boundaries[1]

    @property
    def y_max(self):
        """
        Retrieve the upper boundary in y-direction.

        Returns
        -------
        y_max : float
            In units of [m].
        """
        return self._upper_boundaries[1]

    @property
    def z_min(self):
        """
        Retrieve the lower boundary in z-direction.

        Returns
        -------
        z_min : float
            In units of [m].
        """
        return self._lower_boundaries[2]

    @property
    def z_max(self):
        """
        Retrieve the upper boundary in z-direction.

        Returns
        -------
        z_max : float
            In units of [m].
        """
        return self._upper_boundaries[2]
