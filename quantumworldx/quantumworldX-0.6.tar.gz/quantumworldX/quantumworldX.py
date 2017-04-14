import numpy as np
from matplotlib import pyplot as plt
import matplotlib as mpl


# global variables
COLOR_MAP = 'viridis'

# math utilities


def extend_range(v, percent=0.05):
    vmin, vmax = np.min(v), np.max(v)
    vdiff = (vmax - vmin)
    vmin -= vdiff * percent
    vmax += vdiff * percent
    return vmin, vmax

# time based plotting utilities


def time_colormap(t):
    cmap = mpl.cm.get_cmap(COLOR_MAP)
    norm = mpl.colors.Normalize(vmin=np.min(t), vmax=np.max(t))

    def color_map(v):
        return cmap(norm(v))

    return color_map


def time_colorbar(t):
    cmap = mpl.cm.get_cmap(COLOR_MAP)
    norm = mpl.colors.Normalize(vmin=np.min(t), vmax=np.max(t))
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    # fake up the array of the scalar mappable
    sm._A = []
    return sm


def time_plot(x, y, t, t_step=1):

    cmap = time_colormap(t)

    for indt in range(0, len(t), t_step):
        ti = t[indt]
        plt.plot(x, y[:, indt], c=cmap(ti))

    plt.xlim(extend_range(x))
    plt.ylim(extend_range(y))
    plt.xlabel('$x$')
    plt.ylabel('$y$')

    plt.colorbar(time_colorbar(t), label='time ($t$)',
                 orientation='horizontal')
    return


def time_plot1D(x, t, t_step=1):

    cmap = time_colormap(t)

    for indt in range(0, len(t), t_step):
        ti = t[indt]
        plt.scatter(x[indt], 0, c=cmap(ti), s=100)

    plt.xlim(extend_range(x))
    plt.ylim([-0.5, 0.5])
    plt.xlabel('$x$')
    plt.gca().get_yaxis().set_visible(False)

    plt.colorbar(time_colorbar(t), label='time ($t$)',
                 orientation='horizontal')
    return


# planets simulations
class planet:
    def __init__(self, m, x, v):
        self.mass = m
        self.vel = v
        self.position = x
        self.acceleration = [0, 0]
        self.force = [0, 0]


def update_system(planets, dt):
    compute_acceleration(planets)
    for planet in planets[1:]:  # for each planet
        planet.vel = planet.vel + dt * planet.acceleration
        planet.position = planet.position + dt * planet.vel
    return

# This function updates the acceleration of the planets.


def compute_acceleration(planets):
    n = len(planets)  # total number of planets
    for i in range(n - 1):  # for each pairwise interaction between planets
        for j in range(i + 1, n):
            # Since the first element in the list is a fixed planet (e.g.
            # earth), we don't update the force on it.
            if i == 0:
                rij = np.subtract(planets[i].position, planets[
                                  j].position)  # get a position vector
                # distance between earth and planet j
                distance = np.sqrt(np.dot(rij, rij))
                # get magnitude of force
                magnitude_f = (
                    0.2458 * planets[i].mass * planets[j].mass / np.power(distance, 2))
                # Force vector on planet j
                vect_force = np.multiply(magnitude_f, rij)
                planets[j].force = vect_force
           # calculate the forces between all pairs of planets
            else:
                rij = np.subtract(planets[i].position, planets[
                                  j].position)  # get a position vector
                # distance between two planets and planet j
                distance = np.sqrt(np.dot(rij, rij))
                # get magnitude of force
                magnitude_f = (
                    0.2458 * planets[i].mass * planets[j].mass / np.power(distance, 2))
                # Force vector on planet j
                vect_force = np.multiply(magnitude_f, rij)
                planets[j].force = vect_force + \
                    planets[j].force  # update forces on planet j
                # update forces on planet i
                planets[
                    i].force = np.multiply(-1, vect_force) + planets[i].force

    for i in range(1, n):
        planets[i].acceleration = np.multiply(
            1 / planets[i].mass, planets[i].force)  # a = F/m
    return
# draw planets


def draw_planets(earth, moon_pos, asteroid_pos, rate=10):
    n = len(moon_pos)
    # Axes of figure
    ax = plt.axes(xlim=(-100, 100), ylim=(-100, 100))
    # Add a circle to figure
    ax.add_patch(plt.Circle(earth.position, 10, color='b'))
    # Aspect ration of x and y axes
    ax.set_aspect('equal')
    for i in range(0, n, rate):
        plt.scatter(moon_pos[i, 0], moon_pos[i, 1], c='0.75')
        plt.scatter(asteroid_pos[i, 0], asteroid_pos[i, 1], c='#835C3B')
    plt.show()
    return


# quantum objects


def pib_eigenfunction(x, L, n):
    '''given x, L, and n returns an eigenfunction for the 1D particle in a box
    Inputs: x -- numpy array.
            L -- scalar, length of the box.
            n -- intenger
    '''
    psi_x = np.sqrt(2.0 / L) * np.sin(n * np.pi * x / L)
    return psi_x


def prob_density(psi_x):
    ''' get probability density function associated to the wavefunction psi_x
    Input: psi_x --> an array, representing a values of a wavefunction
    '''
    prob = np.conjugate(psi_x) * psi_x
    return prob


def pib_energy(n, L, h_bar=1, m=1):
    '''This function returns energy of the nth eigenstate
    of the 1D particle in a box.
    Input:
        -- n : quantum number specifying which eigenstate
        -- L, length of the box
    '''
    E_n = (n * h_bar * np.pi) ** 2 / (2.0 * m * L ** 2)
    return E_n


def build_H_matrix(x, v, m=1, h_bar=1):
    ''' this function builds the matrix representation of H,
    given x, the position array, and V_x as input
    '''
    a = x[1] - x[0]  # x is the dx of the grid.  We can get it by taking the diff of the first two
    # entries in x
    t = h_bar ** 2 / (2 * m * a ** 2)  # the parameter t, as defined by schrier

    # initialize H_matrix as a matrix of zeros, with appropriate size.
    H_matrix = np.zeros((len(x), len(x)))
    # Start adding the appropriate elements to the matrix
    for i in range(len(x)):
        # (ONE LINE)
        # Assignt to H_matrix[i][i],the diagonal elements of H
        # The appropriate values
        H_matrix[i][i] = 2 * t + v(x[i])
        #########
        # special case, first row of H
        if i == 0:
            # Assignt to H_matrix[i][i+1],the off-diagonal elements of H
            # The appropriate values, for the first row
            H_matrix[i][i + 1] = -t
        elif i == len(x) - 1:  # special case, last row of H
            H_matrix[i][i - 1] = -t
        else:  # for all the other rows
            # (TWO LINE)
            # Assignt to H_matrix[i][i+1], and H_matrix[i][i-1]
            # the off-diagonal elements of H, the appropriate value, -t
            H_matrix[i][i + 1] = -t
            H_matrix[i][i - 1] = -t
            ################
    return H_matrix

# Isotropic 2D harmonic oscillator


def harmonic_oscillator_2D(xx, yy, l, m, mass=1.0, omega=1.0, hbar=1.0):
    '''Returns the wavefunction for the 1D Harmonic Oscillator, given the following inputs:
    INPUTS:
        xx --> x-axis values for a 2D grid
        yy --> y-axis values for a 2D grid
        l --> l quantum number
        m --> m quantum number
        mass --> mass (defaults to atomic units)
        omega --> oscillator frequency, defaults to atomic units.
        hbar --> planck's constant divided by 2*pi
    '''
    # This is related to how the function np.polynomail.hermite.hermval
    # works.
    coeff_l = np.zeros((l + 1, ))
    coeff_l[l] = 1.0
    coeff_m = np.zeros((m + 1, ))
    coeff_m[m] = 1.0
    # Hermite polynomials required for the HO eigenfunctions
    hermite_l = np.polynomial.hermite.hermval(
        np.sqrt(mass * omega / hbar) * xx, coeff_l)
    hermite_m = np.polynomial.hermite.hermval(
        np.sqrt(mass * omega / hbar) * yy, coeff_m)
    # This is the prefactors in the expression for the HO eigenfucntions
    prefactor = (mass * omega / (np.pi * hbar)) ** (1.0 / 2.0) / \
        (np.sqrt(2 ** l * 2 ** m * misc.factorial(l) * misc.factorial(m)))
    # And the gaussians in the expression for the HO eigenfunctions
    gaussian = np.exp(-(mass * omega * (xx ** 2 + yy ** 2)) / (2.0 * hbar))
    # The eigenfunction is the product of all of the above.
    return prefactor * gaussian * hermite_l * hermite_m

def harmonic_oscillator_wf(x, n, m=1.0, omega=1.0, hbar=1.0):
    '''Returns the wavefunction for the 1D Harmonic Oscillator,
    given the following inputs:
    INPUTS:
        x --> a numpy array
        n --> quantum number, an intenger
        m --> mass (defaults to atomic units)
        omega --> oscillator frequency, defaults to atomic units.
        hbar --> planck's constant divided by 2*pi
    '''
    coeff = np.zeros((n + 1, ))
    coeff[n] = 1.0
    prefactor = 1.0 / (np.sqrt(2 ** n * misc.factorial(n))) * \
        (m * omega / (np.pi * hbar)) ** (1.0 / 4.0)
    gaussian = np.exp(-(m * omega * x * x) / (2.0 * hbar))
    hermite = np.polynomial.hermite.hermval(
        np.sqrt(m * omega / hbar) * x, coeff)
    return prefactor * gaussian * hermite
    
if __name__ == "__main__":
    print("Load me as a module please")
