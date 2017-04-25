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

from __future__ import absolute_import, unicode_literals

import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import numpy as np


def plot_sdcs(x, y, scales=('log', 'log'), marker='bo', fig_ax=None):
    fig, ax = fig_ax or plt.subplots()
    plt.plot(x, y, marker)

    ax.set_ylabel('sdcs')
    ax.set_xscale(scales[0])
    ax.set_yscale(scales[1])

    return fig, ax


def plot_ddcs(x, y, z, scales=('log', 'log', 'log'), fig_ax=None):
    fig, ax = fig_ax or plt.subplots()
    if scales[2] == 'log':
        cs = plt.contourf(x, y, z, norm=LogNorm(vmin=z.min(), vmax=z.max()))
    elif scales[2] == 'linear':
        cs = plt.contourf(x, y, z)
    else:
        raise ValueError('invalid scale: %s' % scales[2])

    cbar = plt.colorbar(cs)
    cbar.ax.set_ylabel('ddcs')
    ax.set_xscale(scales[0])
    ax.set_yscale(scales[1])

    return fig, ax


def generate_data_sdcs(x, cs, *args):
    """
    cs: the cross section function. x must be the first argument of cs.
        args are the remaining arguments to cs.
    """
    x = np.array(x)
    y = cs(x, *args)
    return y


def generate_data_ddcs(x, y, cs, *args):
    """
    cs: the cross section function. x,y must be the first arguments of cs (in that order).
        args are the remaining arguments to cs.
    """
    x, y = np.meshgrid(x, y)
    z = cs(x, y, *args)
    return z


def arange_input(xmin, xmax, npoints, scale='log'):
    if scale == 'log':
        xmin, xmax = np.log10(xmin), np.log10(xmax)
        xstep = (xmax - xmin) / (npoints - 1)
        x = np.array([10 ** (xmin + i * xstep) for i in range(npoints)])
    elif scale == 'linear':
        xstep = (xmax - xmin) / (npoints - 1)
        x = np.array([xmin + i * xstep for i in range(npoints)])
    else:
        raise ValueError('invalid scale: %s' % scale)
    return x
