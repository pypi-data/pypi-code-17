#!/usr/bin/env python
from mpi4py import MPI
import numpy
import os
import cloudpickle


comm = MPI.Comm.Get_parent()
size = comm.Get_size()
rank = comm.Get_rank()


N = numpy.array(0, dtype='i')

spam_p = None
comm.bcast(spam_p, root=0)
print(spam_p)
spam = cloudpickle.loads(spam_p)

comm.Bcast([N, MPI.INT], root=0)
print('worker rank {}, size {}, N {}, pid {}'.format(rank, size, N, os.getpid()))
h = 1.0 / N
s = 0.0
for i in range(rank, N, size):
    x = h * (i + 0.5)
    s += 4.0 / (1.0 + x**2)
    # s += spam(x)
PI = numpy.array(s * h, dtype='d')
comm.Reduce([PI, MPI.DOUBLE], None,
            op=MPI.SUM, root=0)

comm.Disconnect()
