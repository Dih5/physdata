#!/usr/bin/env python3

# Demo: Wrap a fetch function with memoization. Only for python >= 3.2


from physdata.xray import fetch_coefficients
from functools import lru_cache

from time import process_time

fetch_coefficients = lru_cache()(fetch_coefficients)

for x in range(3):
    t = process_time()
    for z in range(1, 10):
        fetch_coefficients(z)
    elapsed_time = process_time() - t
    print(str(x) + " call: " + str(elapsed_time) + " s")
