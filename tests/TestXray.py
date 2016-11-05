#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TestXray.py: Tests for  the `xray` module.
"""

import unittest

from physdata import xray


class TestXray(unittest.TestCase):
    def test_fetch_coefficients(self):
        # Check types in element data
        data = xray.fetch_coefficients(13)
        self.assertTrue(type(data) is list)
        for i in data:
            for j in i:
                self.assertTrue(type(j) is float)
        # Check other format of argument
        self.assertTrue(type(xray.fetch_coefficients("13")) is list)
        self.assertTrue(type(xray.fetch_coefficients("4")) is list)
        self.assertTrue(type(xray.fetch_coefficients(4)) is list)
        # Check a compound
        self.assertTrue(type(xray.fetch_coefficients("tissue")) is list)


    def test_material_lists(self):
        elements = xray.fetch_elements()
        # Test a few
        self.assertTrue(type(elements[0].get_coefficients()) is list)
        self.assertTrue(type(elements[10].get_coefficients()) is list)
        self.assertTrue(type(elements[-1].get_coefficients()) is list)
        compounds = xray.fetch_compounds()
        # Test a few
        self.assertTrue(type(compounds[0].get_coefficients()) is list)
        self.assertTrue(type(compounds[10].get_coefficients()) is list)
        self.assertTrue(type(compounds[-1].get_coefficients()) is list)
        # Test density functionality
        mu_rho = elements[12].get_coefficients(use_density=False)
        mu = elements[12].get_coefficients(use_density=True)
        self.assertAlmostEqual(mu[0][1] / mu_rho[0][1], elements[12].density)
        mu_rho = compounds[12].get_coefficients(use_density=False)
        mu = compounds[12].get_coefficients(use_density=True)
        self.assertAlmostEqual(mu[0][1] / mu_rho[0][1], compounds[12].density)

if __name__ == "__main__":
    unittest.main()
