# -*- coding: utf-8 -*-

#    `ionics` is a software which models various ionization cross sections.
#    Copyright (C) 2017  Dominik Vilsmeier
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

"""
Various classes for random sampling of three-dimensional distributions (specifically double
different ionization cross sections).
"""

import logging

import numpy as np
from scipy.optimize import minimize
import six


class InverseTransformSampling(object):
    """
    Uses inverse transform sampling on a discrete, pre-computed grid. Advantage: The sampling
    process is equally fast, independent of the underlying distribution. Disadvantage: Only
    discrete values are returned.
    """

    def __init__(self, distribution, boundaries_x, boundaries_y):
        """
        Initialize the sampler by pre-computing the distribution on the specified grid.

        Parameters
        ----------
        distribution : callable
            distribution(x, y) should return the distribution's value at (x, y).
        boundaries_x : list or tuple
            (Lower) boundaries of grid cells with respect to x.
        boundaries_y : list or tuple
            (Lower) boundaries of grid cells with respect to y.
        """
        super(InverseTransformSampling, self).__init__()

        def get_xs_and_dxs(boundaries):
            return zip(*[
                [(left + right)/2., right - left]
                for left, right in zip(boundaries[:-1], boundaries[1:])
                ])

        xs, dxs = get_xs_and_dxs(boundaries_x)
        ys, dys = get_xs_and_dxs(boundaries_y)

        x_grid, y_grid = np.meshgrid(xs, ys)
        dx_grid, dy_grid = np.meshgrid(dxs, dys)

        z_grid = distribution(x_grid, y_grid) * dx_grid * dy_grid
        z_prob = z_grid / np.sum(z_grid)

        # Cumulative distribution function with 0 prepended.
        self.cdf = np.insert(np.cumsum(z_prob), 0, [0.])
        self.n_grid_points = len(self.cdf)-1
        self.xs = xs
        self.ys = ys
        self.n_x = len(xs)

    def create_samples(self, count):
        """
        Generate samples from the underlying distribution.

        Parameters
        ----------
        count : int
            Number of samples.

        Returns
        -------
        samples : list[tuple]
            Samples in the form (x, y).
        """
        samples = []
        # noinspection PyTypeChecker
        for r in np.random.random(count):
            i = np.searchsorted(self.cdf, r, side=str('right')) - 1
            x = self.xs[i % self.n_x]
            y = self.ys[i // self.n_x]
            samples.append((x, y))
        return samples


class RejectionSampling(object):
    """
    Uses rejection sampling on a continuous distribution. Advantage: Continuous values are
    returned. Disadvantage: For "wavy" distributions (or rather distributions which are very
    different from being uniform) the sampling process can take a significant amount of time
    as many attempts will be rejected.
    """

    def __init__(self, distribution, x_min, x_max, y_min, y_max):
        """
        Parameters
        ----------
        distribution : callable
            distribution(x, y) should return the distribution's value at (x, y).
        x_min : float
        x_max : float
        y_min : float
        y_max : float
        """
        # Invert function in order to find the maximum via `minimize`.
        # noinspection PyTypeChecker
        result = minimize(
            lambda x: -1. * distribution(x[0], x[1]),
            (1.0, 1.0),
            method='SLSQP',
            bounds=((x_min, x_max), (y_min, y_max)),
            options={'disp': True}
        )
        if not result.success:
            raise StopIteration('Function could not be minimized.')

        log = logging.getLogger('{0}.{1}'.format(__name__, RejectionSampling))
        log.debug('Found maximum at E = %e, T = %e' % (result.x[0], result.x[1]))

        self.max_val = distribution(result.x[0], result.x[1])
        self.distribution = distribution
        self.x_min = x_min
        self.x_range = x_max - x_min
        self.y_min = y_min
        self.y_range = y_max - y_min

    def create_samples(self, count):
        """
        Generate samples from the underlying distribution.

        Parameters
        ----------
        count : int
            Number of samples.

        Returns
        -------
        samples : list[tuple]
            Samples in the form (x, y).
        """
        samples = []
        for _ in six.moves.range(count):
            x = self.x_min + np.random.random() * self.x_range
            y = self.y_min + np.random.random() * self.y_range
            z = np.random.random() * self.max_val
            while z >= self.distribution(x, y):
                x = self.x_min + np.random.random() * self.x_range
                y = self.y_min + np.random.random() * self.y_range
                z = np.random.random() * self.max_val
            samples.append((x, y))
        return samples
