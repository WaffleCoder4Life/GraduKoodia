import matplotlib.pyplot as plt
import statsmodels.api as sm
import scipy.optimize
import numpy as np
from sympy.solvers import solve
from sympy import Symbol
import matplotlib

# Cyro temp
bias_voltage = [23, 23.5, 24, 24.5, 25]
charge_177 = [6.452e5, 7.992e5, 9.601e5, 1.141e6, 1.262e6]
height_177 = [48.68e-3, 59.98e-3, 73.27e-3, 86.53e-3, 100.02e-3]
chargeVariances_177 = [7212804641.634136, 11488199275.871, 11362204858.791971, 11019029374.851696, 15731294021.8476]
heightVariances_177 = [19.189393979174604e-6, 22.106181864009134e-6, 23.29947722562905e-6, 30.567529806792937e-6, 57.80650456546565e-6]

# Cyro temp
charge_114 = [6.958e5, 8.662e5, 1.049e6, 1.215e6, 1.388e6]
height_114 = [55.88e-3, 69.09e-3, 80.82e-3, 93.47e-3, 105.69e-3]
chargeVariances_114 = [10438117743.319704, 9738135644.66893, 9914067545.766144, 12345594056.96445, 10757248453.2531]
heightVariances_114 = [2.6119117591919212e-05, 3.180451489149771e-05, 2.7775641002944193e-05, 3.579135332517678e-05, 2.605218735308991e-05]

# Cyro temp
bias_voltage_955 = [25, 25.5, 26, 26.5, 27]
charge_955 = [2058505.83, 2679292.5 ,3376272.98, 4034768.3, 4784321.85]
height_955 = [0.06663315750000011, 0.08385928600000009 ,0.10052260050000003, 0.11927636699999997, 0.13728641500000008]
chargeVariances_955 = [17424842093.9611, 22432254231.79 ,50375851050.9196, 41948388847.450005, 157004015875.4275]
heightVariances_955 = [2.459890332582704e-05, 2.0248845913135336e-05 ,2.1915163993257338e-05, 2.2464073573900008e-05, 5.929855915790393e-05]

# Room temp
bias_voltage_roomTemp = [26, 26.5, 27, 27.5, 28]
charge_roomTemp = [2106801.91, 2798939.61, 3505097.1, 4292470.91, 5087945.05]
chargeVariance_roomTemp = [40454299551.841896, 70023977664.4779, 532279573918.07, 447997675686.9819, 1119720650161.8875]
height_roomTemp = [0.07340702600000014, 0.09208039050000005, 0.10964822749999993, 0.1309346570000001, 0.14896480550000007]
heightVariance_roomTemp = [2.1424206204771737e-05, 1.834010977286338e-05, 2.9822726844210873e-05, 3.607866361868787e-05, 4.5699885450398736e-05]

# Liquid nitrogen 224 Ohm platinum
bias_voltage_nitrogen = [23, 23.5, 24, 24.5, 25]
charge_nitrogenTemp = [2814346.16, 3407381.64, 4024812.81, 4638770.43, 5249577.99]
chargeVariance_nitrogenTemp = [8288929784.6344, 13140367807.3904, 11480877242.4939, 12404071025.8851, 48588424488.2099]
height_nitrogenTemp = [0.06328231951351586, 0.06717912939343706, 0.07888276189016419, 0.09133768760118186, 0.1011809236088232]
heightVariance_nitrogenTemp = [4.464328552156294e-06, 9.48613702041515e-06, 1.4569162170530072e-05, 1.2365769734924242e-05, 1.630649160160504e-05]

# secound cooling cyckle, 1.174 kOhm
bias_voltage_1174 = [23.5, 24, 24.5, 25, 25.5]
charge_1_174kOhm = [845223.873, 991921.4830000002, 1180063.2659999998, 1361648.53, 1542682.91]
chargeVariance_1_174kOhm = [8896233762.13837, 7266477172.16561, 11710504729.192244, 13618546605.5091, 12980616797.9219]
height_1_174kOhm = [0.06063978083401898, 0.07201918168586344, 0.08440656971737083, 0.09774098751551336, 0.1099117556325746]
heightVariance_1_174kOhm = [1.4928300037418931e-05, 2.0005203519348224e-05, 2.2042494691517947e-05, 2.663945938769572e-05, 3.96173959411806e-05]

# secound cooling cyckle, 1.174 kOhm
bias_voltage_1720 = [23.5, 24, 24.5, 25, 25.5]
charge_1_720kOhm = [779460.8780000003, 964822.7130000001, 1131760.672, 1305792.477, 1540651.24]
chargeVariance_1_720kOhm = [8730141387.792717, 10551729814.28373, 13695522962.674816, 17844497494.731373, 19810637183.5824]
height_1_720kOhm = [0.05914273790902051, 0.07194320179587821, 0.08622401461106112, 0.09858664728645897, 0.11181965277308047]
heightVariance_1_720kOhm = [1.6355056835877525e-05, 1.748797356142702e-05, 2.381084057473337e-05, 2.581058551536464e-05, 2.4902538067833114e-05]

# secound cooling cyckle, 1.174 kOhm, second run
bias_voltage_1720_2 = [23, 23.5, 24, 24.5, 25]
charge_1_720kOhm_2 = [636531.164, 786681.9139999996, 960773.646, 1129894.2069999997, 1327928.264]
chargeVariance_1_720kOhm_2 = [11807525193.372904, 12814142693.985403, 14661608561.172684, 21256569153.47905, 18262271183.943905]
height_1_720kOhm_2 = [0.04881167334629678, 0.05975286214169381, 0.07293559521649144, 0.08584479222662378, 0.09760631416491031]
heightVariance_1_720kOhm_2 = [1.007381716623333e-05, 1.9708098556740163e-05, 2.01815075630937e-05, 1.9582808414541428e-05, 2.0289657034372735e-05]

# second cooling cyckle, 3.750 kOhm
bias_voltage_3_750kOhm = [23, 23.5, 24, 24.5, 25]
charge_3_750kOhm = [611849.5710000001, 771890.3670000001, 943490.9829999997, 1146676.3809999998, 1302952.38]
chargeVariance_3_750kOhm = [11020328060.06226, 8130048798.556612, 11326322909.971611, 13116719957.19034, 14445859822.5156]
height_3_750kOhm = [0.04908070267108466, 0.05671931583672606, 0.07097387105242992, 0.08553262088648214, 0.09799685630195391]
heightVariance_3_750kOhm = [1.1590358431414138e-05, 9.296365306661377e-06, 1.6606453342699748e-05, 1.806259414844926e-05, 2.0297819258620185e-05]

# second cooling cyckle, 3.850 kOhm
bias_voltage_3_850kOhm = [23, 23.5, 24, 24.5, 25]
charge_3_850kOhm = [641271.4504999999, 783263.0495000001, 958372.1249999997, 1084335.6225000003, 1291351.213]
chargeVariance_3_850kOhm = [15331228465.4289, 13752482072.2549, 16448414399.065775, 13572345501.730244, 13381990053.788431]
height_3_850kOhm = [0.04914261221158375, 0.05954371114970103, 0.0723018687711173, 0.07847305022477033, 0.09683659196475858]
heightVariance_3_850kOhm = [1.2077759089759732e-05, 1.6204957018343658e-05, 1.560855580252237e-05, 4.1418161030653236e-06, 9.5666815621758e-06]

# second cooling cyckle, warming up, 1.005 kOhm
bias_voltage_1_005WU = [23, 23.5, 24, 24.5, 25]
charge_1_005kOhmWU = [2739526.17, 3356723.66, 3973208.64, 4582584.92, 5181119.32]
chargeVariance_1_005kOhmWU = [65921338429.8011, 192847237902.7644, 24576855828.9104, 98061767412.3936, 44112237038.8376]
height_1_005kOhmWU = [0.053201686018328885, 0.06566628113206999, 0.07595562129003436, 0.0876387301178458, 0.09941436472083773]
heightVariance_1_005kOhmWU = [8.978446672222226e-06, 1.1212855559968437e-05, 1.659992356330176e-05, 2.506782310884447e-05, 2.7725443323822222e-05]

# warming up, 450 Ohm
WarmUpBias450Ohm = [23, 24, 25]
charge_WarmUpPT450Ohm = [2532320.89, 3824952.2, 5056242.56]
chargeVariance_WarmUpPT450Ohm = [9840520917.9579, 18257887538.08, 38337063691.1264]
height_WarmUpPT450Ohm = [0.05178267535714388, 0.07682973913962378, 0.10189011156787808]
heightVariance_WarmUpPT450Ohm = [1.370396640029773e-05, 1.5589848312676763e-05, 2.2143706272186603e-05]

settings = {
            # CSV file unpacking
            "pathNameDate" : "26042024", # Change to current date
            "measurementID" : "WarmUpPT450Ohm", # Use for example the temperature.
            "csvFileName" : "chargeAndHeightData", # Same name by default

            # Charge and height plottings
            "imageTitle" : "PT 450 $\Omega$",
            "imageFileName" : "WarmUpchargeAndHeightPT450Ohm",

            # Command control
            "plot" : 1,
            "readCSV" : 0,
            "gainPlot" : 0,


}

def run():

    if settings["readCSV"]:
        readCsv(settings)
    
    if settings["gainPlot"]:
        referenceGain()
        gainPlot(charge_roomTemp, chargeVariance_roomTemp, bias_voltage_roomTemp, "Room temperature", "crimson")
        gainPlot(charge_1_720kOhm_2, chargeVariance_1_720kOhm_2, bias_voltage_1720_2, "1.720 kOhm", "magenta")
        gainPlot(charge_3_850kOhm, chargeVariance_3_850kOhm, bias_voltage_3_850kOhm, "3.850 kOhm", "mediumblue")
        plt.savefig("./DataCollection/gainDiffTemp.png")
        plt.show()

    if settings["plot"]:
        chargeAndHeightPlot(charge_WarmUpPT450Ohm, height_WarmUpPT450Ohm, WarmUpBias450Ohm, chargeVariance_WarmUpPT450Ohm, heightVariance_WarmUpPT450Ohm)

# Use for easy list creation. Copy printed lists to save and use data.
def readCsv(settings):
    charge = []
    charge_var = []
    height = []
    height_var = []
    with open("./dataCollection/"+settings["pathNameDate"]+"/"+settings["csvFileName"]+".csv") as file:
        for row in file:
            rowAsList = row.split(",")
            charge.append(float(rowAsList[0]))
            charge_var.append(float(rowAsList[1]))
            height.append(float(rowAsList[2]))
            height_var.append(float(rowAsList[3]))
    print("charge_"+settings["measurementID"]+f" = {charge}")
    print("chargeVariance_"+settings["measurementID"]+f" = {charge_var}")
    print("height_"+settings["measurementID"]+f" = {height}")
    print("heightVariance_"+settings["measurementID"]+f" = {height_var}")

def line(x, a, b):
    return a*x + b
def referenceGain():
    x = Symbol("x")
    voltage = [2.5, 6] 
    gain = [2.9E6, 6.3E6]
    params = scipy.optimize.curve_fit(line, voltage, gain)
    linspace = np.arange(1.5,4.1,0.1)
    line1 = line(linspace, params[0][0], params[0][1])
    plt.plot(linspace, line1, linestyle = "--", label = "Datasheet room temperature")
    plt.legend()

def breakDownVoltCharge(chargeList, chargeVariances, bias_voltage):
    chargeWeight = [1/point for point in chargeVariances]
    
    x = Symbol("x")
    bv = sm.add_constant(bias_voltage)
    chargefit = sm.WLS(chargeList, bv, weights = chargeWeight)
    chargeResult = chargefit.fit()
    line1 = line(x, chargeResult.params[1], chargeResult.params[0])
    breakdownResult = solve(line1, x)
    print(breakdownResult)
    return breakdownResult[0]


def gainPlot(chargeList, chargeVariance, biasVoltageList, label, color):
    electronCharge = 1.6021766E-19
    gainList = []
    for charge in chargeList:
        gainList.append(charge)
    breakDownVoltage = breakDownVoltCharge(chargeList, chargeVariance, biasVoltageList)
    overVoltage = [voltage - breakDownVoltage for voltage in biasVoltageList]
    plt.plot(overVoltage, gainList, marker = "s", color = color, label = label)
    plt.xlabel("Overvoltage / V")
    plt.ylabel("Gain")
    #plt.yscale("log")
    plt.legend()
    # yticks = np.arange(2E6, 7E6, 1E6)
    # print(yticks)
    # plt.yticks(yticks)


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

    voltage_space = np.linspace(19.5, 25.5, 100) # Change to fit bias voltage range
    charge_plot_fit = line(voltage_space, chargeResult.params[1], chargeResult.params[0])
    height_plot_fit = line(voltage_space, heightResult.params[1], heightResult.params[0])

    
    fig, (ax1, ax2) = plt.subplots(nrows=2, sharex=True)

    

    ax1.scatter(bias_voltage, charge, marker = "s", s=10, c="mediumorchid", label="Pulse charge with 1$\sigma$ error bars")
    ax1.errorbar(bias_voltage, charge, yerr=chargeSigmaError, fmt = "none", ecolor = "mediumorchid", capsize = 3)
    ax1.plot(voltage_space, charge_plot_fit, color = "mediumaquamarine", label = "Weighted least squares fit")

    ax1.scatter(breakdownResult, [0], marker = "s", s=10, c="black", label=f"Avalanche breakdown\nvoltage {breakdownResult[0]:.2f} V")
    ax1.errorbar(float(breakdownResult[0]), [0], xerr = [float(breakDownOmega)], fmt = "none", ecolor = "black", capsize = 3)

    ax1.set_ylabel("charge ($10^{6}$ e)")
    ax1.legend()

    ax2.scatter(bias_voltage, height, marker = "s", s=10, c="mediumorchid", label="Pulse height with 1$\sigma$ error bars")
    ax2.errorbar(bias_voltage, height, yerr=heightSigmaError, fmt = "none", ecolor = "mediumorchid", capsize = 3)
    ax2.plot(voltage_space, height_plot_fit, color = "mediumaquamarine", label = "Weighted least squares fit")

    ax2.scatter(breakdownResult2, [0], marker = "s", s=10, c="black", label=f"Avalanche breakdown\nvoltage {breakdownResult2[0]:.2f} V")
    ax2.errorbar(float(breakdownResult2[0]), [0], xerr = [float(breakDownOmega2)], fmt = "none", ecolor = "black", capsize = 3)

    ax2.set_ylabel("pulse height (V)")
    ax2.legend()

    ax1.set_title(settings["imageTitle"])
    plt.xlabel("Bias voltage (V)")
    plt.tight_layout()
    plt.savefig("./dataCollection/"+settings["imageFileName"]+".png")
    plt.show()
    




if __name__ == "__main__":
    run()