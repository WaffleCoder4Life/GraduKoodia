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

bias_voltage_955 = [25, 25.5, 26, 26.5, 27]
charge_955 = [2058505.83, 2679292.5 ,3376272.98, 4034768.3, 4784321.85]
height_955 = [0.06663315750000011, 0.08385928600000009 ,0.10052260050000003, 0.11927636699999997, 0.13728641500000008]
chargeVariances_955 = [17424842093.9611, 22432254231.79 ,50375851050.9196, 41948388847.450005, 157004015875.4275]
heightVariances_955 = [2.459890332582704e-05, 2.0248845913135336e-05 ,2.1915163993257338e-05, 2.2464073573900008e-05, 5.929855915790393e-05]


def line(x, a, b):
    return a*x + b

def chargeAndHeightPlot(charge, height, bias_voltage, chargeVariances, heightVariances):

    chargeWeight = [1/point for point in chargeVariances]
    heightWeight = [1/point for point in heightVariances]

    x = Symbol("x")
    y = Symbol("y")
    bv = sm.add_constant(bias_voltage)
    chargefit = sm.WLS(charge, bv, weights = chargeWeight)
    chargeResult = chargefit.fit()
    line1 = line(x, chargeResult.params[1], chargeResult.params[0])
    breakdownResult = solve(line1, x)
    breakDownOmega = (np.sqrt(chargeResult.cov_params()[0][0]/((chargeResult.params[0])**2)+chargeResult.cov_params()[1][1]/((chargeResult.params[1])**2)-2*(chargeResult.cov_params()[0][1])/(chargeResult.params[0]*chargeResult.params[1]))*breakdownResult[0])
    print(f"Breakdown voltage from charge is {breakdownResult} with standard deviation of {breakDownOmega}")

    heightfit = sm.WLS(height, bv, weights = heightWeight)
    heightResult = heightfit.fit()
    line2 = line(x, heightResult.params[1], heightResult.params[0])
    breakdownResult2 = solve(line2, x)
    breakDownOmega2 = (np.sqrt(heightResult.cov_params()[0][0]/((heightResult.params[0])**2)+heightResult.cov_params()[1][1]/((heightResult.params[1])**2)-2*(heightResult.cov_params()[0][1])/(heightResult.params[0]*heightResult.params[1]))*breakdownResult2[0])
    print(f"Breakdown voltage from height is {breakdownResult2} with standard deviation of {breakDownOmega2}")

    print("Charge fit params: ", chargeResult.params)
    print("Covariant matrix: ", chargeResult.cov_params())
    print("Height fit params: ", heightResult.params)
    print("Covariant matrix: ", heightResult.cov_params())

    chargeSigmaError = [np.sqrt(point) for point in chargeVariances]
    print(f"Charge sigma error: {chargeSigmaError}")
    heightSigmaError = [np.sqrt(point) for point in heightVariances]
    print(f"Height sigma error: {heightSigmaError}")

    voltage_space = np.linspace(22, 28, 100)
    charge_plot_fit = line(voltage_space, chargeResult.params[1], chargeResult.params[0])
    height_plot_fit = line(voltage_space, heightResult.params[1], heightResult.params[0])

    
    fig, (ax1, ax2) = plt.subplots(nrows=2, sharex=True)

    

    ax1.scatter(bias_voltage, charge, marker = "s", s=10, c="mediumorchid", label="Pulse charge with 1$\sigma$ error bars")
    ax1.errorbar(bias_voltage, charge, yerr=chargeSigmaError, fmt = "none", ecolor = "mediumorchid", capsize = 3)
    ax1.plot(voltage_space, charge_plot_fit, color = "mediumaquamarine", label = "Weighted least squares fit")

    ax1.scatter(breakdownResult, [0], marker = "s", s=10, c="black", label=f"Avalanche breakdown voltage")
    ax1.errorbar(float(breakdownResult[0]), [0], xerr = [float(breakDownOmega)], fmt = "none", ecolor = "black", capsize = 3)

    ax1.set_ylabel("charge ($10^{6}$ e)")
    ax1.legend()

    ax2.scatter(bias_voltage, height, marker = "s", s=10, c="mediumorchid", label="Pulse height with 1$\sigma$ error bars")
    ax2.errorbar(bias_voltage, height, yerr=heightSigmaError, fmt = "none", ecolor = "mediumorchid", capsize = 3)
    ax2.plot(voltage_space, height_plot_fit, color = "mediumaquamarine", label = "Weighted least squares fit")

    ax2.scatter(breakdownResult2, [0], marker = "s", s=10, c="black", label=f"Avalanche breakdown voltage")
    ax2.errorbar(float(breakdownResult2[0]), [0], xerr = [float(breakDownOmega2)], fmt = "none", ecolor = "black", capsize = 3)

    ax2.set_ylabel("pulse height (V)")
    ax2.legend()

    ax1.set_title("Temperature 955 $\Omega$")
    plt.xlabel("Bias voltage (V)")
    plt.tight_layout()
    plt.savefig("./dataCollection/charge_and_height_at_955Ohm.png")
    plt.show()
    

chargeAndHeightPlot(charge_955, height_955, bias_voltage_955, chargeVariances_955, heightVariances_955)

