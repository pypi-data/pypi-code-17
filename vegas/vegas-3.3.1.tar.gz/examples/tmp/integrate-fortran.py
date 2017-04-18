import vegas
import math
import numpy as np

import pyximport
pyximport.install(inplace=True)

import c_fcn as fortran


def main():
    integ = vegas.Integrator(2 *[[0,1]])
    f = fortran.f
    warmup = integ(f, neval=3e4, nitn=10, alpha=0.1)
    print warmup.summary()
    results = integ(f, neval=3e4, nitn=10, alpha=0.1)
    print results.summary()

if __name__ == '__main__':
    main()