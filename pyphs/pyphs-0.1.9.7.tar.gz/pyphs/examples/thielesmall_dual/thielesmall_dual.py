#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 11:50:23 2017

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

import os
from pyphs import PHSNetlist, PHSGraph, PHSSimulation, signalgenerator

label = 'thielesmall_dual'

path = os.path.realpath(__file__)[:os.path.realpath(__file__).rfind(os.sep)]

netlist_filename = path + os.sep + label + '.net'

netlist = PHSNetlist(netlist_filename)

graph = PHSGraph(netlist=netlist)

core = graph.buildCore()

if __name__ == '__main__':
    config = {'fs': 48e3,
              'split': True,
              'pbar': True,
              'timer': True,
              'path': path
              }

    simu = PHSSimulation(core, config=config)

    dur = 0.01
    u = signalgenerator(which='sin', f0=800., tsig=dur, fs=simu.fs)

    def sequ():
        for el in u():
            yield (el, )

    simu.init(sequ=sequ(), nt=int(dur*simu.fs))

    simu.process()

    simu.data.plot_powerbal(mode='multi')

    simu.data.plot([('u', 0),
                    ('x', 1),
                    ('x', 0),
                    ('dtx', 0),
                    ('dxH', 2),
                    ('y', 0)])
