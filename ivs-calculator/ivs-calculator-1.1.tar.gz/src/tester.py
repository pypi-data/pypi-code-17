#!/usr/bin/env python3

import unittest
import random
import mathlib


class mlib_test(unittest.TestCase):

    def setUp(self):
        self.solver = mathlib.Solver()

    def test_addition(self):
        self.assertEqual(self.solver.solve('1+1'), 1+1)
        self.assertEqual(self.solver.solve('500.+1820'), 500.+1820)

    def test_multiplicaiton(self):
        self.assertEqual(self.solver.solve('8*300'), 8*300)
        self.assertEqual(self.solver.solve('1.245*2.345'), 1.245*2.345)

    def test_division(self):
        self.assertEqual(self.solver.solve('10/13'), 10/13)
        self.assertEqual(self.solver.solve('8/0'), 'Division by zero!')

    def test_negative(self):
        self.assertEqual(self.solver.solve('0 - 100'), -100)
        self.assertEqual(self.solver.solve('-5 + 1'), -4)
        self.assertEqual(self.solver.solve('-5 * 2'), -10)
        self.assertEqual(self.solver.solve('-5 / 1'), -5)

    def test_priority_multiplication(self):
        task = '2 * 3 + 4'
        self.assertEqual(self.solver.solve(task), 10)
        task = '2 + 3 * 4'
        self.assertEqual(self.solver.solve(task), 14)

    def test_priority_division(self):
        task = '4 / 2 - 2'
        self.assertEqual(self.solver.solve(task), 0)
        task = '4 - 2 / 2'
        self.assertEqual(self.solver.solve(task), 3)

    def test_priority_parentheses(self):
        task = '4 / (2 - 1)'
        self.assertEqual(self.solver.solve(task), 4)
        task = '2 * (3 + 4)'
        self.assertEqual(self.solver.solve(task), 14)

    def test_negative_parentheses(self):
        self.assertEqual(self.solver.solve('-5 + (-10)'), -15)
        self.assertEqual(self.solver.solve('-10 - (-5)'), -5)
        self.assertEqual(self.solver.solve('-10 * (-5)'), 50)
        self.assertEqual(self.solver.solve('10 * (-5)'), -50)
        self.assertEqual(self.solver.solve('-10 * (-0)'), 0)

if __name__ == '__main__':
    unittest.main(verbosity=2)
