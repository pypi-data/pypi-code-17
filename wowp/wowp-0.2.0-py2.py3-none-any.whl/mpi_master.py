#!/usr/bin/env python
from mpi4py import MPI
import numpy
import sys
import os
import cloudpickle
from time import sleep


def spam(x):
    return 4.0 / (1.0 + x**2)


spam_p = cloudpickle.dumps(spam)

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

print('master rank {}, size {}, pid {}'.format(rank, size, os.getpid()))

# comm = MPI.COMM_SELF.Spawn(sys.executable,
#                            args=['mpi_worker.py'],
#                            maxprocs=5)

print('root {}'.format(MPI.ROOT))
sleep(2)
print('bcast 1')
comm.bcast(spam_p, root=MPI.ROOT)

N = numpy.array(100, 'i')
comm.Bcast([N, MPI.INT], root=MPI.ROOT)
PI = numpy.array(0.0, 'd')
comm.Reduce(None, [PI, MPI.DOUBLE],
            op=MPI.SUM, root=MPI.ROOT)
print(PI)

comm.Disconnect()
