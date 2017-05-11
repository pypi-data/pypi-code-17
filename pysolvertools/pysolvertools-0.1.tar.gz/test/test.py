#! /usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import pypond as pond
from copy import deepcopy
from scipy.special import erf


def testpond3d(periodic):
    L = [1.0, 1.0, 1.0]
    N = [32, 64, 128, 256]
    #Np = [256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144, 524288,
    #      1048576, 2097152, 4194304, 8388608, 16777216]
    #err = np.zeros((len(Np),len(N)))
    sigma = 0.1

    """# distribution
    pos = np.array(
        np.random.normal(loc=L[0]/2.0, scale=sigma, size=(4*Np[-1],1)),
        dtype=np.float32)
    weight = np.ones(4*Np[-1], dtype=np.float32)
    # numerical solution
    sol_x = pond.poissonSolverWithDeposit(pos, weight, L, [4*N[-1]], periodic)
    """

    for i in range(10):
        for j in range(len(N)):
            # distribution
            """pos = np.array(
                np.random.normal(loc=L[0]/2.0, scale=sigma, size=(Np[i],3)),
                dtype=np.float32)
            weight = np.ones(Np[i], dtype=np.float32)
            """
            X = np.linspace(0,1,N[j])
            Y = np.linspace(0,1,N[j])
            Z = np.linspace(0,1,N[j])
            X,Y,Z = np.meshgrid(X,Y,Z, indexing='ij')
            rho = np.exp(-0.5*((X-0.5)**2 + (Y-0.5)**2 + (Z-0.5)**2))
            rho = rho.astype(np.float32)
            # numerical solution
            sol = pond.poissonSolver(rho, L, periodic)

            # error
            #err[i,j] = 1.0-np.sqrt((np.sum(sol**2) / np.sum(sol_x**2)))
    print "Computation of the error is not well done"
    #    print err
    """
    plt.figure()
        
    plt.loglog(Np, err)

    plt.figure()
    plt.plot(sol, label='sol')
    #plt.plot(x,rho, label='rho')
    plt.legend()

    plt.show()
    """

def testpond(opt):
    if opt.dim == 1:
        testpond1d(opt.periodic)
    elif opt.dim == 2:
        testpond2d(opt.periodic)
    elif opt.dim == 3:
        testpond3d(opt.periodic)
    else:
        print "Dim not defined"


        
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-dim",
                        action="store",
                        dest="dim",
                        default=3,
                        type=int,
                        help="Number of dimension",
                        metavar="INT")

    parser.add_argument("-periodic",
                        action="store",
                        dest="periodic",
                        default=1,
                        type=int,
                        help="Test with periodic boundaries",
                        metavar="INT")
    
    opt = parser.parse_args()
    testpond(opt)

