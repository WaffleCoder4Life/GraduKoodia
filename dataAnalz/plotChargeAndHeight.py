import matplotlib.pyplot as plt
import statsmodels.api as sm
import scipy.optimize
import numpy as np
from sympy.solvers import solve
from sympy import Symbol


bias_voltage = [23, 23.5, 24, 24.5, 25]
charge_177 = [6.452e5, 7.992e5, 9.601e5, 1.141e6, 1.262e6]
height_177 = [48.68e-3, 59.98e-3, 73.27e-3, 86.53e-3, 100.02e-3]
chargeVariances_177 = [7212804641.634136, 11488199275.871, 11362204858.791971, 11019029374.851696, 15731294021.8476]
heightVariances_177 = [19.189393979174604e-6, 22.106181864009134e-6, 23.29947722562905e-6, 30.567529806792937e-6, 57.80650456546565e-6]

charge_114 = [6.958e5, 8.662e5, 1.049e6, 1.215e6, 1.388e6]
height_114 = [55.88e-3, 69.09e-3, 80.82e-3, 93.47e-3, 105.69e-3]
chargeVariances_114 = [10438117743.319704, 9738135644.66893, 9914067545.766144, 12345594056.96445, 10757248453.2531]
heightVariances_114 = [2.6119117591919212e-05, 3.180451489149771e-05, 2.7775641002944193e-05, 3.579135332517678e-05, 2.605218735308991e-05]


def line(x, a, b):
    return a*x + b

def chargeAndHeightPlot(charge, height, bias_voltage, chargeVariances, heightVariances):

    chargeWeight = [1/point for point in chargeVariances]
    heightWeight = [1/point for point in heightVariances]

    x = Symbol("x")
    bv = sm.add_constant(bias_voltage)
    chargefit = sm.WLS(charge, bv, weights = chargeWeight)
    chargeResult = chargefit.fit()
    line1 = line(x, chargeResult.params[1], chargeResult.params[0])
    breakdownResult = solve(line1, x)
    print(f"Breakdown voltage from charge is {breakdownResult}")
    heightfit = sm.WLS(height, bv, weights = heightWeight)
    heightResult = heightfit.fit()
    line2 = line(x, heightResult.params[1], heightResult.params[0])
    breakdownResult = solve(line2, x)
    print(f"Breakdown voltage from height is {breakdownResult}")

    print("Charge fit params: ", chargeResult.params)
    print("Covariant matrix: ", chargeResult.cov_params())
    print("Height fit params: ", heightResult.params)
    print("Covariant matrix: ", heightResult.cov_params())

    chargeSigmaError = [np.sqrt(point) for point in chargeVariances]
    print(f"Charge sigma error: {chargeSigmaError}")
    heightSigmaError = [np.sqrt(point) for point in heightVariances]
    print(f"Height sigma error: {heightSigmaError}")

    voltage_space = np.linspace(20, 26, 100)
    charge_plot_fit = line(voltage_space, chargeResult.params[1], chargeResult.params[0])
    height_plot_fit = line(voltage_space, heightResult.params[1], heightResult.params[0])

    
    fig, (ax1, ax2) = plt.subplots(nrows=2, sharex=True)

    

    ax1.scatter(bias_voltage, charge, marker = "s", s=10, c="mediumorchid", label="Pulse charge with 1$\sigma$ error bars")
    ax1.errorbar(bias_voltage, charge, yerr=chargeSigmaError, fmt = "none", ecolor = "mediumorchid", capsize = 3)
    ax1.plot(voltage_space, charge_plot_fit, color = "mediumaquamarine", label = "Weighted least squares fit")
    ax1.set_ylabel("charge ($10^{6}$ e)")
    ax1.legend()

    ax2.scatter(bias_voltage, height, marker = "s", s=10, c="mediumorchid", label="Pulse height with 1$\sigma$ error bars")
    ax2.errorbar(bias_voltage, height, yerr=heightSigmaError, fmt = "none", ecolor = "mediumorchid", capsize = 3)
    ax2.plot(voltage_space, height_plot_fit, color = "mediumaquamarine", label = "Weighted least squares fit")
    ax2.set_ylabel("pulse height (V)")
    ax2.legend()

    ax1.set_title("Temperature 1.77 k$\Omega$")
    plt.xlabel("Bias voltage (V)")
    plt.tight_layout()
    plt.savefig("./dataCollection/charge_and_height_at_177kOhm.png")
    plt.show()
    

chargeAndHeightPlot(charge_177, height_177, bias_voltage, chargeVariances_177, heightVariances_177)

