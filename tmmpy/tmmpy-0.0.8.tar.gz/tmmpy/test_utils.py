import matplotlib.pylab as plt
import time

from tmmpy_core import *
from tmmpy_objects import *


# region Sample stacks

def sample_stack_tmp():
    s = Stack()
    s.append(Layer(Material(1.0, 0), 500))
    s.append(Layer(Material(2.0, 1e-2), 1000))
    s.append(Layer(Material(1.0, 1e-2), 1000))
    s.append(Layer(Material(3.0, 1e-2), 500))
    s.append(Layer(Material(1.0, 0), 500))
    return s


def sample_stack():
    s = Stack()
    s.append(Layer(Material(1.5, 0.002), 500))
    s.append(Layer(Material(2.0, 0.006), 500))
    s.append(Layer(Material(2.5, 0.001), 500))
    s.append(Layer(Material(2.0, 0.006), 500))
    s.append(Layer(Material(1.5, 0.002), 500))
    s.right = Material(2.0, 0.0)
    return s


def sample_stack_simple():
    s = Stack()
    s.append(Layer(Material(1.0, 0.0), 500))
    s.append(Layer(Material(1.5, 0.0), 500))
    s.append(Layer(Material(1.0, 0.0), 500))
    s.right = Material(1.0, 0.0)
    return s


def sample_stack_small():
    s = Stack()
    s.append(Layer(Material(1.0, 0.0), 500))
    s.append(Layer(Material(2.5, 0.0), 500))
    s.right = Material(1.5, 0.0)
    return s


def sample_stack_large():
    s = Stack()
    s.append(Layer(Material(1.5, 0), 500))
    s.append(Layer(Material(2.0, 0), 500))
    s.append(Layer(Material(2.5, 0), 500))
    s.append(Layer(Material(4.0, 0), 500))
    s.append(Layer(Material(2.0, 0), 500))
    s.append(Layer(Material(3.0, 0), 500))
    s.append(Layer(Material(1.5, 0), 500))
    s.right = Material(2.0, 0.0)
    return s


def sample_stack_complex():
    s = Stack()
    s.append(Layer(Material(1.5, 0.002), 500))
    s.append(Layer(Material(2.0, 0.001), 500))
    s.append(Layer(Material(2.5, 0.004), 500))
    s.append(Layer(Material(4.0, 0.001), 500))
    s.append(Layer(Material(2.0, 0.006), 500))
    s.append(Layer(Material(3.0, 0.002), 500))
    s.append(Layer(Material(1.5, 0.001), 500))
    s.right = Material(2.0, 0.0)
    return s


def sample_stacks():
    return [sample_stack_simple(), sample_stack_small(), sample_stack_large(), sample_stack_complex()]


# endregion

def check_energy_cons_incoh(s, delta, debug=True):
    return check_energy_cons(s, delta, ['i'] * len(s), debug)


def check_energy_cons_mixed(s, delta, debug=True):
    return test_mixed(s, lambda coh_lst: check_energy_cons(s, delta, coh_lst, debug))


def test_abs_from_phi_incoh(s, visual):
    return test_abs_from_phi(s, visual, ['i'] * len(s), "incoherent")


def test_abs_from_phi_mixed(s, visual):
    return test_mixed(s, lambda coh_lst: test_abs_from_phi(s, visual, coh_lst, "mixed"))


def check_energy_cons(s, delta, coh_lst=None, debug=True):
    lmb = 500
    pts = [[i + 1, 100] for i in range(len(s))]
    success = True
    for pol in ['s', 'p']:
        # Check that phi decreases through the structure.
        points, phi = scan_flux_asm(s, lmb, pol, 0, coh_lst, pts)
        diffs = np.diff(phi)
        success = success and np.all(diffs < delta)
        if debug and np.any(np.diff(phi) > delta):
            # Do debug stuff.
            plt.plot(points, phi)
            plt.ylim(0, 2)
            plt.show()
    return 0 if success else 1


def test_abs_from_phi(s, visual, coh_lst=None, name=None):
    lmb = 250
    pts = [[i + 1, 500] for i in range(len(s))]
    error = 0
    for pol in ['s', 'p']:
        # Compare abs calculated (1) analytically (2) numerically from phi, coherent case.
        points, abs_asm = scan_abs_asm(s, lmb, pol, 0, coh_lst, pts)
        points, phi_asm = scan_flux_asm(s, lmb, pol, 0, coh_lst, pts)
        # points, phi_asm = scan_flux_asm(s, lmb, pol, 0, coh_lst, pts)
        dx = points[1] - points[0]
        abs_from_phi = -np.diff(phi_asm) / dx
        abs_matching = array(np.add(abs_asm[1:], abs_asm[:-1])) / 2
        # Compare the two graphs using RMS.
        rel_err_sq = ((abs_from_phi - abs_matching) / abs_matching) ** 2
        if visual:
            plt.clf()
            plt.subplot(2, 1, 1)
            plt.plot(points, phi_asm)
            plt.subplot(2, 1, 2)
            plt.plot(array(points[:-1]), abs_from_phi)
            plt.plot(array(points[:-1]), abs_matching)
        if visual: plt.savefig(
            '{}_{}.png'.format(name if name is not None else "coherent", int(round(time.time() * 1000))))
        error += np.sqrt(np.mean(rel_err_sq))
    return error / 2.0


def test_layer_abs(s, coh_lst=None):
    result = solve_asm(s, 500, 's', 0, coh_lst)
    abs_all = 1 - result['R'][0] - result['T'][0]
    # Compare TOTAL absorption (energy conservation)
    result = layer_abs_asm(s, [500], 's', 0, coh_lst)
    return abs(abs_all - np.sum(result[0][1:-1]))


def test_mixed(s, test):
    error = 0
    for i in xrange(len(s)):
        coh_lst = ['c'] * len(s)
        coh_lst[i] = 'i'
        error = error + test(coh_lst)
        incoh_lst = ['c'] * len(s)
        incoh_lst[i] = 'i'
        error = error + test(incoh_lst)
    return error / len(s)
