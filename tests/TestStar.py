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


if __name__ == "__main__":
    unittest.main()
