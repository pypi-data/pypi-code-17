import unittest
import test_utils as tu

from tmmpy_core import *
from tmmpy_objects import *


class TestCoherent(unittest.TestCase):
    def test_sanity(self):
        self.assertTrue(True)

    def test_transparent_layer(self):
        lmb = 500
        s = Stack()
        air = Material(1, 0)
        s.append(Layer(air, 1000))
        result = solve_tmm(s, lmb, 's', 0)
        self.assertAlmostEqual(result['T'][0], 1.0)
        self.assertAlmostEqual(result['R'][0], 0.0)
        result = solve_tmm(s, lmb, 'p', 0)
        self.assertAlmostEqual(result['T'][0], 1.0)
        self.assertAlmostEqual(result['R'][0], 0.0)

    def test_glass_reflection(self):
        lmb = 500
        s = Stack()
        glass = Material(1.5, 0)
        s.right = glass
        result = solve_tmm(s, lmb, 's', 0)
        self.assertAlmostEqual(result['T'][0], 0.96)
        self.assertAlmostEqual(result['R'][0], 0.04)
        result = solve_tmm(s, lmb, 'p', 0)
        self.assertAlmostEqual(result['T'][0], 0.96)
        self.assertAlmostEqual(result['R'][0], 0.04)

    def test_metal_reflection(self):
        lmb = 500
        s = Stack()
        silver = Material(0.15, 3.00)
        s.right = silver
        # Numbers from Byrnes tmm package.
        result = solve_tmm(s, lmb, 's', 0)
        self.assertAlmostEqual(result['T'][0], 0.0581254541051)
        self.assertAlmostEqual(result['R'][0], 0.941874545895)
        result = solve_tmm(s, lmb, 'p', 0)
        self.assertAlmostEqual(result['T'][0], 0.0581254541051)
        self.assertAlmostEqual(result['R'][0], 0.941874545895)

    def test_anti_reflection_coating(self):
        n = 1.5
        lmb = 500
        # Build structure.
        s = Stack()
        s.right = Material(n, 0)
        s.append(Layer(Material(np.sqrt(n), 0), lmb / 4 / np.sqrt(n)))
        # In the coherent case, all light will be transmitted.
        result = solve_tmm(s, lmb, 's', 0)
        self.assertAlmostEqual(result['T'][0], 1.0)
        self.assertAlmostEqual(result['R'][0], 0.0)

    def test_energy_cons_phi_coherent(self):
        # Lossless structures (e.g. energy flow constant)
        self.assertEquals(tu.check_energy_cons(tu.sample_stack_small(), 1e-15, debug=False), 0)
        self.assertEquals(tu.check_energy_cons(tu.sample_stack_simple(), 1e-15, debug=False), 0)
        self.assertEquals(tu.check_energy_cons(tu.sample_stack_large(), 1e-15, debug=False), 0)
        # Lossy structures (e.g. energy flow decreasing)
        self.assertEquals(tu.check_energy_cons(tu.sample_stack(), 0, debug=False), 0)
        self.assertEquals(tu.check_energy_cons(tu.sample_stack_complex(), 0, debug=False), 0)

    def test_abs_from_phi_coherent(self):
        s = tu.sample_stack()
        self.assertAlmostEqual(tu.test_abs_from_phi(s, False), 0, 1)

    def test_layer_abs(self):
        for s in tu.sample_stacks():
            self.assertAlmostEquals(tu.test_layer_abs(s), 0)

    def test_e_vec_interface_continuity(self):
        lmb = 500
        s = tu.sample_stack()
        for pol in ['s', 'p']:
            for ang in array([0.0, 40.0, 70.0])/180.0*np.pi:
                # Calculate vector fields.
                result = solve_tmm(s, lmb, pol, ang, {'E': eval_E_coherent})
                pre = pre_process(s, lmb, ang)
                for i in range(1, len(s) + 1):
                    beta = phase_shift(lmb, pre['n'][i], pre['d'][i], pre['ang'][i])
                    left = E_vec_from_E(np.dot(coherent_propagation_matrix(beta), result['E'][0][i]), pol, pre['ang'][i])
                    right = E_vec_from_E(result['E'][0][i-1], pol, pre['ang'][i-1])
                    # Test continuity of tangential component of E-field.
                    self.assertAlmostEqual(right[0], left[0])
                    self.assertAlmostEqual(right[1], left[1])
                    # Test continuity of parallel component of D-field.
                    self.assertAlmostEqual(right[2]*pre['n'][i-1]**2, left[2]*pre['n'][i]**2)
