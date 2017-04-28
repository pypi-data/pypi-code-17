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

from ionics.sdcs import bethe
from ionics.sdcs import voitkiv as voitkiv_single
from ionics.ddcs import voitkiv as voitkiv_double

import plots
import matplotlib.pyplot as plt
import sys

fig_ax = plt.subplots()


def test_sdcs_bethe_non_rel():
    sdcs_bethe = bethe.BetheNonRel()
    sdcs_bethe.prepare(1.e6, 1, 'H')

    E = plots.arange_input(0.1, 100, 100)
    sdcs_data = plots.generate_data_sdcs(E, sdcs_bethe)
    plots.plot_sdcs(E, sdcs_data, fig_ax=fig_ax)


def test_sdcs_bethe_rel():
    sdcs_bethe = bethe.BetheRel()
    sdcs_bethe.prepare(1.e9, 1, 'H')

    E = plots.arange_input(0.1, 100, 100)
    sdcs_data = plots.generate_data_sdcs(E, sdcs_bethe)
    plots.plot_sdcs(E, sdcs_data, fig_ax=fig_ax)


def test_sdcs_voitkiv_E():
    sdcs_voitkiv = voitkiv_single.VoitkivE()
    sdcs_voitkiv.prepare(1.e9, 1, 'H')

    E = plots.arange_input(0.1, 100, 100)
    sdcs_data = plots.generate_data_sdcs(E, sdcs_voitkiv)
    plots.plot_sdcs(E, sdcs_data, marker='rx', fig_ax=fig_ax)


def test_sdcs_voitkiv_T():
    sdcs_voitkiv = voitkiv_single.VoitkivT()
    sdcs_voitkiv.prepare(1.e9, 1, 'H')

    T = plots.arange_input(0, 3.1415, 100, scale='linear')
    sdcs_data = plots.generate_data_sdcs(T, sdcs_voitkiv)
    plots.plot_sdcs(T, sdcs_data, scales=('linear', 'log'), fig_ax=fig_ax)


def test_ddcs_voitkiv():
    ddcs_voitkiv = voitkiv_double.Voitkiv()
    ddcs_voitkiv.prepare(1.e9, 1, 'H')

    E = plots.arange_input(0.1, 100, 100)
    T = plots.arange_input(0, 3.1415, 100, scale='linear')
    ddcs_data = plots.generate_data_ddcs(E, T, ddcs_voitkiv)
    plots.plot_ddcs(E, T, ddcs_data, scales=('log', 'linear', 'log'), fig_ax=fig_ax)


# exec(sys.argv[1])

test_sdcs_bethe_rel()
# test_sdcs_voitkiv_E()
plt.show()
