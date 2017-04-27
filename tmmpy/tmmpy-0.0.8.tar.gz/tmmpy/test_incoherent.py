import unittest
import test_utils as tu

from tmmpy_core import *
from tmmpy_objects import *


class TestIncoherent(unittest.TestCase):
    def test_sanity(self):
        self.assertTrue(True)

    def test_transparent_layer(self):
        lmb = 500
        s = Stack()
        air = Material(1, 0)
        s.append(Layer(air, 1000))
        result = solve_asm(s, lmb, 's', 0, ['i'])
        self.assertAlmostEqual(result['T'][0], 1.0)
        self.assertAlmostEqual(result['R'][0], 0.0)
        result = solve_asm(s, lmb, 'p', 0, ['i'])
        self.assertAlmostEqual(result['T'][0], 1.0)
        self.assertAlmostEqual(result['R'][0], 0.0)

    def test_anti_reflection_coating(self):
        n = 1.5
        lmb = 500
        # Build structure.
        s = Stack()
        s.right = Material(n, 0)
        s.append(Layer(Material(np.sqrt(n), 0), lmb / 4 / np.sqrt(n)))
        # Numbers from Byrnes tmm package.
        result = solve_asm(s, lmb, 's', 0, ['i'])
        self.assertAlmostEqual(result['T'][0], 0.979795897113)
        self.assertAlmostEqual(result['R'][0], 0.0202041028867)

    def test_abs_from_phi_incoherent(self):
        self.assertAlmostEqual(tu.test_abs_from_phi_incoh(tu.sample_stack(), False), 0, 1)

    def test_energy_cons_phi_incoherent(self):
        # Lossless structures (e.g. energy flow constant)
        self.assertEquals(tu.check_energy_cons_incoh(tu.sample_stack_small(), 1e-15, debug=False), 0)
        self.assertEquals(tu.check_energy_cons_incoh(tu.sample_stack_simple(), 1e-15, debug=False), 0)
        self.assertEquals(tu.check_energy_cons_incoh(tu.sample_stack_large(), 1e-15, debug=False), 0)

        # Lossy structures (e.g. energy flow decreasing)
        self.assertEquals(tu.check_energy_cons_incoh(tu.sample_stack(), 0, debug=False), 0)
        self.assertEquals(tu.check_energy_cons_incoh(tu.sample_stack_complex(), 0, debug=False), 0)

    def test_layer_abs_incoherent(self):
        for s in tu.sample_stacks():
            self.assertAlmostEquals(tu.test_layer_abs(s, ['i'] * len(s)), 0, 6)

    def test_abs_from_phi_mixed(self):
        self.assertAlmostEqual(tu.test_abs_from_phi_mixed(tu.sample_stack(), False), 0, 1)

    def test_energy_cons_phi_mixed(self):
        # Lossless structures (e.g. energy flow constant)
        self.assertEquals(tu.check_energy_cons_mixed(tu.sample_stack_small(), 1e-15, debug=False), 0)
        self.assertEquals(tu.check_energy_cons_mixed(tu.sample_stack_simple(), 1e-15, debug=False), 0)
        self.assertEquals(tu.check_energy_cons_mixed(tu.sample_stack_large(), 1e-15, debug=False), 0)

        # Lossy structures (e.g. energy flow decreasing)
        self.assertEquals(tu.check_energy_cons_mixed(tu.sample_stack(), 0, debug=False), 0)
        self.assertEquals(tu.check_energy_cons_mixed(tu.sample_stack_complex(), 0, debug=False), 0)

    def test_layer_abs_mixed(self):
        for s in tu.sample_stacks():
            error = tu.test_mixed(s, lambda coh_lst: tu.test_layer_abs(s, coh_lst))
            self.assertAlmostEquals(error, 0, 6)
