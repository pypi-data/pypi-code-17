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

if __name__ == "__main__":
    print("Load me as a module please")
