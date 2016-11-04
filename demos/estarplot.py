#!/usr/bin/env python

# Demo: Plot some estar data

from physdata import star
import matplotlib.pyplot as plt
import numpy as np

data_13 = np.array(star.fetch_estar("013"))
data_82 = np.array(star.fetch_estar("082"))
plt.loglog(data_13[:, [0]], data_13[:, [4]], label="Al")
plt.loglog(data_82[:, [0]], data_82[:, [4]], label="Pb")
plt.xlabel("Energy (MeV)")
plt.ylabel("CSDA range (g/cm^2)")
plt.legend()
plt.show()
