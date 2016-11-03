#!/usr/bin/env python

# Demo: Plot x-ray attenuation data

from physdata.xray import *
import matplotlib.pyplot as plt
import numpy as np

data = np.array(fetch_coefficients(13))
print(data)
plt.loglog(data[:, [0]], data[:, [1]], label=r"$\mu/\rho$")
plt.loglog(data[:, [0]], data[:, [2]], label=r"$\mu_{\mathrm{en}}/\rho$")
plt.xlabel("Energy (MeV)")
plt.ylabel("Coefficient (cm^2/g)")
plt.legend()
plt.show()
