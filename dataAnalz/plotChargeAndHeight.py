import matplotlib.pyplot as plt
import statsmodels.api as sm
import scipy.optimize
import numpy as np


bias_voltage = [23, 23.5, 24, 24.5, 25]
charge = [6.452e+05, 7.992e+05, 9.601e+05, 1.141e+06, 1.262e+06]
height = [48.68e-3, 59.98e-3, 73.27e-3, 86.53e-3, 100.02e-3]
variances = [15921933698.355574, 19336130353.702526, 20114644263.632584, 17079539900.205984, 22067120899.00696]

weight = [1/point for point in variances]

bv = sm.add_constant(bias_voltage)

chargefit = sm.WLS(charge, bv, weights=weight)
result = chargefit.fit()

print("Charge fit params: ", result.params)
print("Covariant matrix: ", result.cov_params())

def line(x, a, b):
    return a*x + b

sigma_error = [np.sqrt(point) for point in variances]

voltage_space = np.linspace(20, 26, 100)
charge_plot_fit = line(voltage_space, result.params[1], result.params[0])




fig, (ax1, ax2) = plt.subplots(nrows=2, sharex=True)

ax1.scatter(bias_voltage, charge, marker = "s", s=10, c="mediumorchid", label="Pulse charge with one sigma error bars")
ax1.errorbar(bias_voltage, charge, yerr=sigma_error, fmt = "none", ecolor = "mediumorchid", capsize = 3)
ax1.plot(voltage_space, charge_plot_fit, color = "mediumaquamarine", label = "WLS fit")
ax1.legend()

ax2.scatter(bias_voltage, height, marker = "s", s=10, c="mediumorchid", label="Pulse height")

plt.tight_layout()
plt.show()