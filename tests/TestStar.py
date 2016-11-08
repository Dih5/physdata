#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TestStar.py: Tests for the `star` module.
"""

import unittest

from physdata import star


class TestStar(unittest.TestCase):
    def test_fetch_star_type(self):
        # Test type of return
        for data in [star.fetch_estar(13), star.fetch_astar(13), star.fetch_pstar(13)]:
            self.assertTrue(type(data) is list)
            for i in data[0]:
                self.assertTrue(type(i) is float)

    def test_fetch_star_input(self):
        # Test formats for argument
        for f in [star.fetch_estar, star.fetch_astar, star.fetch_pstar]:
            self.assertEqual(f(1), f("1"))
            self.assertEqual(f(13), f("13"))
            self.assertEqual(f(101), f("101"))

    def test_fetch_star_density(self):
        # Test density scaling
        for f in [star.fetch_estar, star.fetch_astar, star.fetch_pstar]:
            no_density = f(13)
            density_2 = f(13, density=2.0)
            auto_density = f(13, density=True)
            for x, y, z in zip(no_density, density_2, auto_density):
                # Energy is not scaled
                self.assertAlmostEqual(x[0], y[0])
                self.assertAlmostEqual(x[0], z[0])
                # Last value is not scaled
                self.assertAlmostEqual(x[-1], y[-1])
                self.assertAlmostEqual(x[-1], z[-1])
                # Stopping power (of a certain kind) is scaled
                self.assertAlmostEqual(x[1] * 2, y[1])
                self.assertAlmostEqual(x[1] * 2.6989, z[1])  # The Aluminium density in the website
                # Ranges are scaled by the inverse
                self.assertAlmostEqual(x[4] / 2, y[4])
                self.assertAlmostEqual(x[4] / 2.6989, z[4])  # The Aluminium density in the website


if __name__ == "__main__":
    unittest.main()
