from pyswmm import Simulation
from datetime import datetime

with Simulation('TestModel4_toolkitUnits.inp') as sim:
    sim.start_time = datetime(2011,1,1,0,0,0)
    sim.end_time = datetime(2011,1,2,0,0,0)
    sim.step_advance(300)
    for step in sim:
        print sim.current_time
    sim.report()

