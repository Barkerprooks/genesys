#!/usr/bin/env python3

import csv
import statistics
import matplotlib.pyplot as plt

with open('./planets.csv', newline='') as file:
    reader = csv.DictReader(file)
    masses, radii = [], []

    for row in reader:
        masses.append(float(row['mass']) * 1.899e+27) # in km
        radii.append(float(row['radius']) * 7.1492e7) # in meters

masses.sort()
radii.sort()

mass_std = statistics.stdev(masses)
radius_std = statistics.stdev(radii)

mass_mid = masses[len(masses) // 2]
radius_mid = radii[len(radii) // 2]

print('mass:', mass_mid, mass_std)
print('radius:', radius_mid, radius_std)

# in the future, may use these as the RNG distribution
masses = masses[:1200] # try to cut off outliers
plt.plot(masses)
plt.title('masses')
plt.show()

radii = radii[:1200]
plt.plot(radii)
plt.title('radii')
plt.show()