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

"""
This module provides components that model the particle generation process.
Models which incorporate ionization can refer to the sub-package :mod:`ionization` which
contains several related classes.
Models which incorporate gas motion can refer to the sub-package :mod:`gas_dynamics` which
contains several related classes.
"""

from __future__ import absolute_import, print_function, unicode_literals

import abc

from anna import Integer, PhysicalQuantity, String, Triplet, \
    depends_on, parametrize
import injector
import numpy
import pandas
import scipy.constants as constants
import six

import virtual_ipm.di as di
from virtual_ipm.components import Model
from virtual_ipm.simulation.simulation import Progress

from .ionization.cross_sections import SimpleDDCS, VoitkivModel


# noinspection PyOldStyleClasses
class ParticleGenerationModel(Model):
    """
    (Abstract) Base class for particle generation models.

    A particle generation model represents a way of how particles enter the simulation cycle.
    For IPM simulations this most frequently incorporates the ionization process induced by
    the interaction of a beam with the rest gas. However other ways of generating particles are
    possible. For example for studying secondary electron emission emerging from ion impact on
    detector elements one would use a model which generates particles based on the output of
    a previous simulation which tracked the ions towards the detector.
    """

    CONFIG_PATH_TO_IMPLEMENTATION = 'ParticleGeneration/Model'
    CONFIG_PATH = 'ParticleGeneration/Parameters'

    def __init__(self, particle_supervisor, configuration=None):
        """
        Initialize the particle generation model.

        Parameters
        ----------
        particle_supervisor : :class:`ParticleSupervisor`
        configuration : :class:`ConfigurationAdaptor` derived class
        """
        super(ParticleGenerationModel, self).__init__(configuration)
        self._particle_supervisor = particle_supervisor

    def create_particle(self, progress, position=None, momentum=None):
        """
        Proxy method for creating a particle via  :method:`ParticleSupervisor.create_particle`.

        Parameters
        ----------
        progress : :class:`Progress`
        position : :class:`~numpy.ndarray` or list or tuple, optional
        momentum : :class:`~numpy.ndarray` or list or tuple, optional
        """
        return self._particle_supervisor.create_particle(
            progress, position=position, momentum=momentum
        )

    @abc.abstractmethod
    def generate_particles(self, progress):
        """
        Generate particles and set the initial values for position and momentum. This method
        must be implemented by particle generation models.

        Parameters
        ----------
        progress : :class:`Progress`
            The current simulation progress at which the particles are generated.
        """
        raise NotImplementedError

Interface = ParticleGenerationModel


# noinspection PyOldStyleClasses
@parametrize(
    Integer(
        'SimulationStep',
        info='The simulation step at which the particle will be created.',
        for_example=0
    ) >= 0,
    Triplet[PhysicalQuantity](
        'Position',
        unit='m',
        info='The position at which the particle will be created.',
        for_example=(0., 0., 0.)
    ).use_container(numpy.array),
    Triplet[PhysicalQuantity](
        'Velocity',
        unit='m/s',
        info='The velocity with which the particle will be created.',
        for_example=(0., 0., 0.)
    ).use_container(numpy.array)
)
class SingleParticle(ParticleGenerationModel):
    """
    This model creates a single particle at the specified simulation step with position and 
    velocity initially set to the specified parameters. This is particularly useful for testing
    setups and quickly observing a particle trajectory.
    """

    @injector.inject(
        configuration=di.components.configuration,
        particle_supervisor=di.components.particle_supervisor,
        setup=di.components.setup
    )
    def __init__(self, configuration, particle_supervisor, setup):
        super(SingleParticle, self).__init__(particle_supervisor, configuration)
        self._mass = setup.particle_type.mass

    def generate_particles(self, progress):
        if progress.step == self._simulation_step:
            self.create_particle(progress, self._position, self._mass * self._velocity)


# noinspection PyOldStyleClasses
@parametrize(
    String('Filepath')
)
class DirectPlacementModel(ParticleGenerationModel):
    """
    This model allows for specifying a set of particles via their initial parameters and they will
    be accordingly created during the simulation. The file needs to be given as a CSV file with
    the following columns (in this exact order)::

        simulation step, x, y, z, vx, vy, vz

    Column delimiter is "," (comma). An arbitrary number of lines in this format may be given.
    Particles are created during the specified simulation step with the specified initial position
    and velocity.
    
    .. note::
       The first line is a header line and must reflect the above given column structure.
    
    .. warning::
       Only non-relativistic velocities are allowed.
    """

    column_names = ('simulation step', ' x', ' y', ' z', ' vx', ' vy', ' vz')

    @injector.inject(
        configuration=di.components.configuration,
        particle_supervisor=di.components.particle_supervisor,
        setup=di.components.setup
    )
    def __init__(self, configuration, particle_supervisor, setup):
        super(DirectPlacementModel, self).__init__(particle_supervisor, configuration)
        self._mass = setup.particle_type.mass
        self._data_frame = pandas.DataFrame.from_csv(self._filepath, index_col=None)
        self._steps = self._data_frame.iloc[:, 0]

    def as_json(self):
        return super(DirectPlacementModel, self).as_json()

    def generate_particles(self, progress):
        to_be_generated_indices = numpy.argwhere(self._steps == progress.step).flatten()
        for index in to_be_generated_indices:
            position = numpy.array(self._data_frame.iloc[index, 1:4], dtype=float)
            momentum = numpy.array(self._data_frame.iloc[index, 4:7], dtype=float) * self._mass
            self.create_particle(progress, position, momentum)


# noinspection PyOldStyleClasses
class ZZeroZeroMomentum(ParticleGenerationModel):
    """
    This model generates all particles at ``z=0`` with zero momentum (i.e. at rest). The transverse
    positions are sampled according to the Bunch's transverse charge distribution.
    """

    @injector.inject(
        beams=di.components.beams,
        particle_supervisor=di.components.particle_supervisor,
        setup=di.components.setup,
        configuration=di.components.configuration
    )
    def __init__(self, beams, particle_supervisor, setup, configuration):
        super(ZZeroZeroMomentum, self).__init__(particle_supervisor, configuration)
        self._beams = beams
        self._setup = setup
        self._number_of_ionizations = setup.number_of_particles
        self._ionization_ratios = None
        self._longitudinal_density_arrays = None
        self._n_particles_cache = {}

    def prepare(self):
        # Generated particles are proportional to
        # population * gas_density * ionization_cross_section.
        ionization_ratios = numpy.array(list(map(
            lambda beam_: beam_.bunch_population * beam_.total_ionization_cross_section,
            self._beams
        )))
        self._ionization_ratios = ionization_ratios / numpy.sum(ionization_ratios)
        self.log.debug('Ionization ratios: %s', self._ionization_ratios)

        # noinspection PyUnresolvedReferences
        progresses = list(map(
            lambda step: Progress(step, self._setup.number_of_time_steps, self._setup.time_delta),
            six.moves.range(self._setup.number_of_time_steps)
        ))
        longitudinal_density_arrays = []
        for beam in self._beams:
            long_density_array = numpy.array(list(map(
                lambda progress: abs(beam.charge_density_at(
                    numpy.array(
                        [progress.time * constants.speed_of_light, 0., 0., 0.]
                    )[:, numpy.newaxis],
                    progress
                )),
                progresses
            ))).flatten()
            if numpy.sum(long_density_array) > 0.:
                long_density_array /= numpy.sum(long_density_array)
            else:
                self.log.warning(
                    'Charge density of beam %s is zero at z=0 during the simulation time range'
                )
            longitudinal_density_arrays.append(long_density_array)
            self.log.debug('Longitudinal density array: %s', long_density_array.tolist())
        self._longitudinal_density_arrays = longitudinal_density_arrays

    def compute_number_of_particles_to_be_created(self, progress):
        # Need to cache result because the number of particles to be created is determined using
        # random number generation for the fractional part and because this function is called from
        # both position and momentum generation it could potentially lead to different numbers.
        if progress.step in self._n_particles_cache:
            return self._n_particles_cache[progress.step]
        n_particles_per_beam = []
        for beam, long_density, ratio in zip(
                self._beams,
                self._longitudinal_density_arrays,
                self._ionization_ratios):
            n_particles = self._number_of_ionizations * long_density[progress.step] * ratio
            fraction = n_particles - int(n_particles)
            n_particles_per_beam.append(
                int(n_particles) + (numpy.random.random() < fraction)
            )
        self.log.debug(
            'Creating %s particles at step %d', n_particles_per_beam, progress.step
        )
        self._n_particles_cache[progress.step] = n_particles_per_beam
        return n_particles_per_beam

    def generate_positions(self, progress):
        positions = []
        for beam, n_particles in zip(
                self._beams,
                self.compute_number_of_particles_to_be_created(progress)):
            if n_particles > 0:
                # Generate positions at z=0.
                positions.append(
                    beam.generate_positions_in_transverse_plane(progress, n_particles, 0.)
                )
        if not positions:
            return numpy.empty((0,))
        positions_as_array = positions[0]
        for pos in positions[1:]:
            positions_as_array = numpy.concatenate((positions_as_array, pos), axis=-1)
        return positions_as_array

    # noinspection PyUnusedLocal,PyMethodMayBeStatic
    def generate_momenta(self, progress):
        count = sum(self.compute_number_of_particles_to_be_created(progress))
        n_particles = self.compute_number_of_particles_to_be_created(progress)
        return numpy.zeros((3, count), dtype=float)

    def generate_particles(self, progress):
        positions = self.generate_positions(progress)
        momenta = self.generate_momenta(progress)
        if positions.size == 0:
            assert momenta.size == 0, 'Momenta generated while no positions were generated'
            return
        # noinspection PyUnresolvedReferences
        for nr in six.moves.range(positions.shape[1]):
            self.create_particle(
                progress,
                position=positions[:, nr],
                momentum=momenta[:, nr]
            )


# noinspection PyOldStyleClasses
@depends_on(
    VoitkivModel
)
class ZZeroVoitkivMomentum(ZZeroZeroMomentum):
    """
    This model generates all particles at ``z=0`` with momenta sampled from the Voitkiv DDCS.
    The transverse positions are sampled according to the Bunch's transverse charge distribution.
    """

    @injector.inject(
        beams=di.components.beams,
        particle_supervisor=di.components.particle_supervisor,
        setup=di.components.setup,
        configuration=di.components.configuration
    )
    def __init__(self, beams, particle_supervisor, setup, configuration):
        super(ZZeroVoitkivMomentum, self).__init__(
            beams=beams,
            particle_supervisor=particle_supervisor,
            setup=setup,
            configuration=configuration
        )
        self._beams = beams
        self._setup = setup
        self._ratios = None
        self._longitudinal_density_arrays = None
        self._ionization_cross_sections = list(map(
            lambda beam: VoitkivModel(
                beam,
                setup,
                configuration.get_configuration(self.CONFIG_PATH)
            ),
            self._beams
        ))

    def as_json(self):
        return dict(
            super(ZZeroVoitkivMomentum, self).as_json(),
            ionization_cross_sections=list(map(
                lambda ics: ics.as_json(),
                self._ionization_cross_sections
            ))
        )

    def prepare(self):
        super(ZZeroVoitkivMomentum, self).prepare()
        for ics in self._ionization_cross_sections:
            ics.prepare()

    def generate_momenta(self, progress):
        momenta = []
        for ics, count in zip(
                self._ionization_cross_sections,
                self.compute_number_of_particles_to_be_created(progress)):
            momenta.append(ics.generate_momenta(count))
        if not momenta:
            return numpy.empty((0,))
        momenta_as_array = momenta[0]
        for momentum in momenta[1:]:
            momenta_as_array = numpy.concatenate((momenta_as_array, momentum), axis=-1)
        return momenta_as_array


# Inherits from ZZeroVoitkivMomentum because it already has the required ionization cross section
# functionality; we simply override the ionization cross sections as they all follow a common
# interface. However this abstract functionality could be moved to a separate class and enabled
# via multiple inheritance. Or alternatively insert this additional ionization cross section class
# above ZZeroVoitkivMomentum in the class hierarchy and make ZZeroGeneratorSimpleDDCS inherit from
# this class rather than from ZZeroVoitkivMomentum.
# noinspection PyOldStyleClasses
@depends_on(
    SimpleDDCS
)
class ZZeroSimpleDDCS(ZZeroVoitkivMomentum):
    """
    This model generates all particles at ``z=0`` with momenta sampled from a decoupled DDCS.
    The transverse positions are sampled according to the Bunch's transverse charge distribution.
    """

    @injector.inject(
        beams=di.components.beams,
        configuration=di.components.configuration,
        particle_supervisor=di.components.particle_supervisor,
        setup=di.components.setup
    )
    def __init__(self, beams, particle_supervisor, setup, configuration):
        super(ZZeroSimpleDDCS, self).__init__(
            beams=beams,
            particle_supervisor=particle_supervisor,
            setup=setup,
            configuration=configuration
        )
        # Override the ionization cross sections here; the required generate_momenta functionality
        # is generally applicable and already available.
        self._ionization_cross_sections = list(map(
            lambda beam: SimpleDDCS(
                setup,
                configuration.get_configuration(self.CONFIG_PATH)
            ),
            self._beams
        ))

# Because ZZeroSimpleDDCS inherits from ZZeroVoitkivMomentum it retains the dependency on
# VoitkivModel which is not required in this case. Inheritance was applied only for obtaining
# functionality.
setattr(ZZeroSimpleDDCS, '_depends_on_%s' % VoitkivModel.__name__, None)
