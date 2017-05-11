"""
PyPond is a N dimensional poisson solver.
It contains a three essentials methods in solving poisson:
 * A poisson solver
 * A weight deposit (computing the density from particles)
 * An interpolation of the potential/forces

It uses numpy's array, fft and interpolation and is coded in C.
A parallel version will be available soon
"""

import _pysolvertools
import numpy
from scipy.interpolate import interpn

def deposit(pos, weight, L, N, O=None, periodic=1):
    """
    Compute the density from particles.
    Uses a linear deposit scheme (other orders may become available later).
    :ref:'Np' is the number of particles and :ref:'dim' is the number of dimension.
    :param np.array(Np,dim) pos: Position of each particles
    :param np.array(Np) weight: Weight to deposit
    :param tuple(dim) O: Origin of the system
    :param tuple(dim) L: Size of the system
    :param tuple(dim) N: Discretization for the mesh
    :param bool periodic: Periodic boundaries or isolated
    :returns: np.array(N) density
    """
    l = tuple(numpy.array(L,dtype=float))
    n = tuple(N)
    if O is None:
        o = l
    else:
        o = tuple(O)
    return _pysolvertools.deposit(pos, weight, o, l, n, periodic)

def poissonSolver(rho, L, periodic=1):
    """
    Solve the poisson equation :math:'\phi = \Delta rho'.
    In the 1D case, the isolated case is solved by a LU decomposition.
    The other cases are done with a FFT (if periodic) or the SSOR
    algorithm (otherwise).
    :ref:'N' is the discretization (see :ref:'deposit').
    :param np.array(N) rho: density (charge, mass, ...)
    :param tuple(L) L: System size
    :param bool periodic: Periodic boundaries or isolated
    :returns: np.array(N) Potential (phi)
    """
    l = tuple(numpy.array(L,dtype=float))
    dim = len(rho.shape)
    if periodic or dim == 1:
        # solve poisson
        return _pysolvertools.poissonSolver(rho, l, periodic)
    else:
        tmp = numpy.zeros(2*numpy.array(rho.shape))
        if dim == 2:
            tmp[:rho.shape[0],:rho.shape[1]] = rho
        elif dim == 3:
            tmp[:rho.shape[0],:rho.shape[1],:rho.shape[2]] = rho
            l = tuple(2*numpy.array(l))
            # solve poisson
        phi = _pysolvertools.poissonSolver(rho, l, 1)
        if dim == 2:
            return phi[:rho.shape[0],:rho.shape[1]]
        elif dim == 3:
            return phi[:rho.shape[0],:rho.shape[1],:rho.shape[2]]        

def poissonSolverWithDeposit(pos, weight, L, N, O=None, periodic=1):
    """
    Solve the poisson equation :math:'\phi = \Delta rho'.
    First do a :ref:'deposit', then :ref:'poissonSolver'.
    :ref:'Np' is the number of particles and :ref:'dim' is the number of dimension.
    :param np.array(Np,dim) pos: Position of each particles
    :param np.array(Np) weight: Weight to deposit
    :param tuple(dim) O: Origin of the system
    :param tuple(dim) L: Size of the system
    :param tuple(dim) N: Discretization for the mesh
    :param bool periodic: Periodic boundaries or isolated
    :returns: np.array(N) Potential (phi)
    """
    rho = deposit(pos, weight, L, N, O, periodic)
    return poissonSolver(rho, L, periodic)

def getPotential(phi, pos, L, O=None, grid=None):
    """
    Compute the potential at the given positions.
    Use a linear interpolation.
    :ref:'Np' is the number of position and :ref:'dim' is the number of dimension.
    :param np.array(N) phi: Potential
    :param np.array(Np,dim) pos: Positions
    :param tuple(dim) O: Origin of the system
    :param tuple(L) L: System size
    :param np.array(N) grid: Grid for the system or None
    :returns: np.array(Np) Potential
    """
    if O is None:
        O = [0.0]*len(L)
    if grid is None:
        grid = [] # grid
        for i in range(len(phi.shape)):
            grid.append(numpy.linspace(O[i],L[i]+O[i],phi.shape[i]))
    return interpn(grid, phi, pos, method='linear')


def getAcceleration(phi, pos, L, O=None, grid=None):
    """
    Compute the acceleration due to the field at the given positions.
    Use a nearest interpolation.
    :ref:'Np' is the number of position and :ref:'dim' is the number of dimension.
    :param np.array(N) phi: Potential
    :param np.array(Np,dim) pos: Positions
    :param tuple(dim) O: Origin of the system
    :param tuple(L) L: System size
    :param np.array(N) grid: Grid for the system or None
    :returns: np.array(Np,dim) Acceleration
    """
    if O is None:
        O = [0.0]*len(L)
    acc = np.empty_as(pos)
    # compute the grid
    if grid is None:
        grid = [] # grid
        for i in range(len(phi.shape)):
            grid.append(numpy.arange(O[i],O[i]+L[i],phi.shape[i]))

    # compute stepsize
    dx = []
    for i in range(len(phi.shape)):
        dx.append(L/(phi.shape[i]-1.0))
    
    # compute the acceleration on the mesh
    grad = numpy.gradient(phi,*dx)
    # compute the acceleration at the required position
    for i in range(len(phi.shape)):
        acc[:,i] = interpn(grid, grad[i], pos, method='nearest')
    return acc

def getPotentialFromDeposit(pos, weight, L, N, O=None, periodic=1):
    """
    Compute the potential at the given positions.
    See :ref:'poissonSolverWithDeposit' and :ref:'getPotential' for more information.
    :ref:'Np' is the number of particles and :ref:'dim' is the number of dimension.
    :param np.array(Np,dim) pos: Position of each particles
    :param np.array(Np) weight: Weight to deposit
    :param tuple(dim) O: Origin of the system
    :param tuple(dim) L: Size of the system
    :param tuple(dim) N: Discretization for the mesh
    :param bool periodic: Periodic boundaries or isolated
    :returns: np.array(Np) Potential
    """
    phi = poissonSolverWithDeposit(pos, weight, L, N, O, periodic)
    return getPotential(phi, pos, L, O)

def getAccelerationFromDeposit(pos, weight, L, N, O=None, periodic=1):
    """
    Compute the acceleration at the given positions.
    See :ref:'poissonSolverWithDeposit' and :ref:'getAcceleration' for more information.
    :ref:'Np' is the number of particles and :ref:'dim' is the number of dimension.
    :param np.array(Np,dim) pos: Position of each particles
    :param np.array(Np) weight: Weight to deposit
    :param tuple(dim) O: Origin of the system
    :param tuple(dim) L: Size of the system
    :param tuple(dim) N: Discretization for the mesh
    :param bool periodic: Periodic boundaries or isolated
    :returns: np.array(Np) Acceleration
    """
    phi = poissonSolverWithDeposit(pos, weight, L, N, O, periodic)
    return getAcceleration(phi, pos, L, O)
