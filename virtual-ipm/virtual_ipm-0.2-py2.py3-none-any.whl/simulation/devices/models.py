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

import abc

from anna import PhysicalQuantity, Duplet, parametrize
import injector
import numpy

from virtual_ipm.components import Model
import virtual_ipm.di as di


class DeviceModel(Model):
    """
    (Abstract) Base class for device models.

    A device model is responsible for

    * defining the boundaries of the simulation region. This information is for example used by
      bunch electric field models in order to confine the volume in which the field must be
      precomputed.
    * deciding when particles are detected or invalidated (invalidated means a particle stopped
      tracking but was not detected; e.g. it hit the boundary of the chamber).

    The task of identifying which particles are detected is a very general one and extends
    for example to the use case of studying BIF monitors. The device would compute
    the decay probabilities per particle and use this information in order to determine when
    the particle is considered detected.

    Status updates must not be performed manually via assignment but using the dedicated methods
    provided by this base class instead:

    * :method:`Device.invalidate`
    * :method:`Device.detect`

    This is because for each status update a corresponding status update notification will be
    generated and published on the :method:`ParticleSupervisor.status_updates` stream.
    When using manual assignment those notifications are not created.
    """

    CONFIG_PATH_TO_IMPLEMENTATION = 'Device/Model'
    CONFIG_PATH = 'Device/Parameters'

    def __init__(self, particle_supervisor, configuration=None):
        """
        Initialize the device model.

        Parameters
        ----------
        particle_supervisor : :class:`ParticleSupervisor`
        configuration : :class:`ConfigurationAdaptor` derived class
        """
        super(DeviceModel, self).__init__(configuration)
        self._particle_supervisor = particle_supervisor

    def invalidate(self, particles, progress):
        """
        Set the status of the given particles to "invalid".

        Parameters
        ----------
        particles : :class:`ParticleIndexView`
        progress : :class:`Progress`
            The current simulation progress at which the status change happens.
        """
        self.log.debug('Particles invalidated: %s', particles)
        if particles:
            self._particle_supervisor.invalidate(particles, progress)

    def detect(self, particles, progress):
        """
        Set the status of the given particles to "detected".

        Parameters
        ----------
        particles : :class:`ParticleIndexView`
        progress : :class:`Progress`
            The current simulation progress at which the status change happens.
        """
        self.log.debug('Particles detected: %s', particles)
        if particles:
            self._particle_supervisor.detect(particles, progress)

    @abc.abstractmethod
    def scan_particles(self, particles, progress):
        """
        Check the given particles and change their statuses if appropriate.
        This method must be implemented by all Device subclasses.

        Parameters
        ----------
        particles : :class:`ParticleIndexView`
        progress : :class:`Progress`
            The current simulation progress at which this method is invoked.
        """
        raise NotImplementedError

    @abc.abstractproperty
    def lower_boundaries(self):
        """
        The lower boundaries of the device.

        .. note::
        ``lower_boundaries < upper_boundaries`` for each dimension.

        Returns
        -------
        lower_boundaries : :class:`~numpy.ndarray`, shape (3,)
            In units of [m].
        """
        raise NotImplementedError

    @abc.abstractproperty
    def upper_boundaries(self):
        """
        The upper boundaries of the device.

        .. note::
        ``upper_boundaries > lower_boundaries`` for each dimension.

        Returns
        -------
        upper_boundaries : :class:`~numpy.ndarray`, shape (3,)
            In units of [m].
        """
        raise NotImplementedError

Interface = DeviceModel


@parametrize(
    Duplet[PhysicalQuantity](
        'LowerBoundaries',
        unit='m',
        info='Give only x and y; z is ignored.'
    ).use_container(numpy.array),
    Duplet[PhysicalQuantity](
        'UpperBoundaries',
        unit='m',
        info='Give only x and y; z is ignored.'
    ).use_container(numpy.array)
)
class BasicIPM(DeviceModel):
    """
    Allows for specification of upper and lower boundaries with respect to x- and y-direction.
    The detector is located at the lower y-boundary. When particles reach this level they are
    considered detected.
    """

    @injector.inject(
        particle_supervisor=di.components.particle_supervisor,
        configuration=di.components.configuration
    )
    def __init__(self, particle_supervisor, configuration):
        super(BasicIPM, self).__init__(particle_supervisor, configuration)

    @property
    def lower_boundaries(self):
        return self._lower_boundaries

    @property
    def upper_boundaries(self):
        return self._upper_boundaries

    def scan_particles(self, particles, progress):
        # Detector is located at lower_boundaries[1] (= y).
        # noinspection PyTypeChecker
        self.invalidate(
            particles[
                numpy.any(
                    particles.position[:-1].T >= self.upper_boundaries,
                    axis=1
                )
            ],
            progress
        )
        self.invalidate(
            particles[particles.x <= self.lower_boundaries[0]],
            progress
        )
        self.detect(
            particles[particles.y <= self.lower_boundaries[1]],
            progress
        )


class InterpolatingIPM(BasicIPM):
    __doc__ = BasicIPM.__doc__.rstrip() + """
    This device model uses the current and the previous position of particles in order to
    interpolate their final positions at the detector level.
    """

    @injector.inject(
        particle_supervisor=di.components.particle_supervisor,
        configuration=di.components.configuration,
        setup=di.components.setup
    )
    def __init__(self, particle_supervisor, configuration, setup):
        super(InterpolatingIPM, self).__init__(particle_supervisor, configuration)
        self._dt = setup.time_delta

    def detect_particle(self, particles, progress):
        # Interpolate final positions at detector level.
        inverse_y_slope = self._dt / (particles.y - particles.previous_y)
        delta_time_to_detector = (
            inverse_y_slope
            * (self.lower_boundaries[1] - particles.previous_y)
        )
        slopes = (particles.position - particles.previous_position) / self._dt
        particles.position = particles.previous_position + slopes * delta_time_to_detector
        super(InterpolatingIPM, self).detect_particle(particles, progress)
