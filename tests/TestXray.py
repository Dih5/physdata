#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TestXray.py: Tests for  the `xray` module.
"""

import unittest

from physdata import xray

from urllib.error import HTTPError


class TestXray(unittest.TestCase):
    def test_fetch_coefficients(self):
        # Check types in element data
        data = xray.fetch_coefficients(13)
        self.assertIsInstance(data, list)
        for i in data:
            for j in i:
                self.assertIsInstance(j, float)
        # Check other format of argument
        self.assertIsInstance(xray.fetch_coefficients("13"), list)
        self.assertIsInstance(xray.fetch_coefficients("4"), list)
        self.assertIsInstance(xray.fetch_coefficients(4), list)
        # Check a compound
        self.assertIsInstance(xray.fetch_coefficients("tissue"), list)

        # Check requesting non existing data raises exceptions
        with self.assertRaises(HTTPError):
            xray.fetch_coefficients("mithril")
        with self.assertRaises(HTTPError):
            xray.fetch_coefficients(999)

    def test_material_lists(self):
        elements = xray.fetch_elements()
        # Test a few
        self.assertIsInstance(elements[0].get_coefficients(), list)
        self.assertIsInstance(elements[10].get_coefficients(), list)
        self.assertIsInstance(elements[-1].get_coefficients(), list)
        compounds = xray.fetch_compounds()
        # Test a few
        self.assertIsInstance(compounds[0].get_coefficients(), list)
        self.assertIsInstance(compounds[10].get_coefficients(), list)
        self.assertIsInstance(compounds[-1].get_coefficients(), list)
        # Test density functionality
        mu_rho = elements[12].get_coefficients(use_density=False)
        mu = elements[12].get_coefficients(use_density=True)
        self.assertAlmostEqual(mu[0][1] / mu_rho[0][1], elements[12].density)
        mu_rho = compounds[12].get_coefficients(use_density=False)
        mu = compounds[12].get_coefficients(use_density=True)
        self.assertAlmostEqual(mu[0][1] / mu_rho[0][1], compounds[12].density)

if __name__ == "__main__":
    unittest.main()