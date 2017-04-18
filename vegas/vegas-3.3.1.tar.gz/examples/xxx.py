import numpy as np
import vegas

np.random.seed((1,3))   # causes reproducible random numbers

def main():
    integ = vegas.Integrator(4 * [[0, 1]], ran_sync=True)
    # adapt
    # f = vegas.batchintegrand(ridge.fbatch)
    integ(f2, nitn=10, neval=1e5)
    # final results
    result = integ(f2, nitn=10, neval=1e5)
    if integ.mpi_rank == 0:
        # result should be approximately 0.851
        print('result = %s    Q = %.2f' % (result, result.Q))

def f(x):
    dim = 4
    N = 1000
    ans = 0
    fac = (100. / 3.1415926535897932384626) ** 2
    for j in range(N):
        x0 = j / (N - 1.)
        dx2 = 0.0
        for d in range(dim):
            dx2 += (x[d] - x0) ** 2
        ans += np.exp(-100. * dx2)
    return ans * fac / N

def f2(x):
    N = 1000
    dim = 4
    ans = 0
    fac = (100. / 3.1415926535897932384626) ** 2
    x0 = np.arange(0., N) / (N - 1.)
    dx2 = 0.0
    for d in range(dim):
        dx2 += (x[d] - x0) ** 2
    return np.sum(np.exp(-100 * dx2)) * fac / N

if __name__ == '__main__':
    main()
