#!/usr/bin/env python3

import cProfile
from mathlib import Solver
import math
from random import random

psets = [[int(random()*100) for _ in range(10**x)] for x in range(4, 7)]

solver = Solver()

for i in psets:
    profiler = cProfile.Profile()
    print('Profiling mathlib.std (standard deviation): 10^',
          int(math.log10(len(i))), ' numbers', sep='')
    profiler.runcall(solver.std, i)
    profiler.print_stats()
