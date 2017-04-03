# This file is part of xrayutilities.
#
# xrayutilities is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.
#
# Copyright (C) 2015 Dominik Kriegner <dominik.kriegner@gmail.com>

import unittest

import xrayutilities as xu
import numpy


class TestFuzzyGridder1D(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.num = numpy.random.randint(10, 99)
        cls.xmin = 1
        cls.xmax = cls.num
        cls.x = numpy.linspace(cls.xmin, cls.xmax, num=cls.num)
        cls.data = numpy.random.rand(cls.num)
        cls.gridder = xu.FuzzyGridder1D(cls.num)
        cls.gridder(cls.x, cls.data, width=2)

    def test_gridder1d_axis(self):
        # test length of xaxis
        self.assertEqual(len(self.gridder.xaxis), self.num)
        # test values of xaxis
        for i in range(self.num):
            self.assertAlmostEqual(self.gridder.xaxis[i], self.x[i], places=12)

    def test_gridder1d_data(self):
        # test length of data
        self.assertEqual(len(self.gridder.data), self.num)
        # test values of data
        for i in [0, -1]:
            v = 0.75 * self.data[i] + 0.25 * self.data[i+2*i+1]
            self.assertAlmostEqual(self.gridder.data[i], v, places=12)
        for i in range(1, self.num-1):
            v = 0.25 * (self.data[i-1] + self.data[i+1]) + 0.5 * self.data[i]
            self.assertAlmostEqual(self.gridder.data[i], v, places=12)

if __name__ == '__main__':
    unittest.main()
