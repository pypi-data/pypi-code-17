#!/usr/bin/env python3

import cProfile
import mathlib
import math
from random import random

profile_sets = [[int(random()*100) for _ in range(10**x)] for x in range(4,7)]

solver = mathlib.solver()

for i in profile_sets:
    profiler = cProfile.Profile()
    print('Profiling mathlib.std (standard deviation): 10^', int(math.log10(len(i))), ' numbers', sep='')
    profiler.runcall(solver.std, i)
    profiler.print_stats()
