import numpy as np
import scipy.optimize
from scipy import stats
from scipy.special import laguerre
import math
import matplotlib.pyplot as plt
from collections import Counter
from scipy.optimize import curve_fit


settings = {

    "pathNameDate" : "26042024",
    "fileName" : "HeightListMath",
    "plotName" : "photonDistributionLED5Vbias",
    "biasVoltage" : "23",
    "numberOfDatasets" : 5000,

    "plotPoissonFit" : 0,
    "countLEDplot" : 0,
    "poissonParameterFit" : 0, # Shit no work
    "plotPoissonHeight" : 0,

}

# 3.72 kOhm temperature, photon counts at different LED voltages
LEDvolt = [5.5, 5.6, 5.7, 5.8, 5.9, 6]
meanCount = [3.276, 3.903, 4.612, 5.437, 6.037, 6.928]


def modifiedPoissonian(n, l, q):
    return ((1-q)*q**n)/((np.exp(l))-1)#*(laguerre(n)(-l*((1-q)/q))-1)

xdata = np.linspace(1,5,5)
ydata = [modifiedPoissonian(point, 1.4, 0.21) for point in xdata]
print(ydata)
print(xdata)
plt.scatter(xdata, ydata)
plt.show()


def line(x,a,b):
    return a*x+b

def poissonParameterFit(settings):
    with open("./dataCollection/"+settings["pathNameDate"]+"/"+settings["fileName"]+settings["biasVoltage"]+".csv", "r") as file:
        photonDistribution = []
        for row in file:
            if row == '\n':
                pass
            else:
                photonDistribution.append(float(row.strip("\n")))
    # Count mean value of photons
    photonCounts = Counter(photonDistribution)
    countList = []
    xdata = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0]
    for key in xdata:
        countList.append(photonCounts[key])
    print(countList)
    bounds = [(0,10) , (0,1)]
    res = stats.fit(modifiedPoissonian, countList, bounds)
    print(res.params)


def plotPoissonFit(settings):


    with open("./dataCollection/"+settings["pathNameDate"]+"/"+settings["fileName"]+settings["biasVoltage"]+".csv", "r") as file:
        photonDistribution = []
        for row in file:
            if row == '\n':
                pass
            else:
                photonDistribution.append(float(row.strip("\n")))
    # Count mean value of photons
    photonCounts = Counter(photonDistribution)
    print(photonCounts)
    poisson_lambda = 0
    for key in photonCounts:
        poisson_lambda += int(key)*int(photonCounts[key])
    poisson_lambda /= settings["numberOfDatasets"]
    print(f"Mean value of photons {poisson_lambda}")
    poisdata = np.random.poisson(poisson_lambda, 10000*settings["numberOfDatasets"])

    labels, counts = np.unique(photonDistribution, return_counts=True)
    
    plt.bar(labels, counts, width = 1, color = "darkorange", edgecolor = "black", align='center', linestyle = "--", label = "measurement")
    labels = [point for point in range(-1, len(counts), 1)]
    plt.gca().set_xticks(labels)
    
    labels2, counts2 = np.unique(poisdata, return_counts=True)
    counts2 = [point/10000 for point in counts2[:18]]
    labels2 = [point for point in range(-1, len(labels2), 1)]
    counts2.insert(0, 0)
    plt.step(labels2, counts2, "k", linewidth = 1, where = "mid", label = "Poissonian fit $\\mathrm{\\lambda}$="+str(poisson_lambda))

    # FIXED POISSON
    counts3 = []
    n=0
    fixed_lambda = round(poisson_lambda,4)
    while n < 12:
        counts3.append(modifiedPoissonian(fixed_lambda, 0.1, n))
        n+=1

    print(counts3)
    counts3 = [point*settings["numberOfDatasets"] for point in counts3]
    labels3 = [point for point in range(-1, len(counts3)-1, 1)]
    plt.bar(labels3, counts3, width = 1, color = "steelblue", edgecolor = "black", align = "center", linestyle = ":", alpha = 0.5, label = "Fixed poissonian $\\lambda$="+str(fixed_lambda))

    
    plt.title("Bias voltage "+settings["biasVoltage"]+" V, 5000 pulses")
    plt.xlabel("photoelectron")
    plt.ylabel("counts")
    plt.legend()
    plt.xlim(-0.5,len(counts))
    #plt.savefig("./dataCollection/"+str(settings["pathNameDate"])+"/Photos/"+settings["plotName"]+settings["biasVoltage"]+".png")
    plt.show()

def plotPoissonHeight(settings):
    heightList = []
    # with open("./dataCollection/"+settings["pathNameDate"]+"/"+settings["fileName"]+settings["biasVoltage"]+".csv", "r") as file:
    #     for row in file:
    #         heightList.append(float(row.strip()))
    # heightList = [round(point,1) for point in heightList]
    # heightCounts = Counter(heightList)
    # heightCounts = dict(sorted(heightCounts.items()))

    with open("./dataCollection/"+settings["pathNameDate"]+"/"+settings["fileName"]+settings["biasVoltage"]+".csv", "r") as file:
        for row in file:
            if float(row.strip()) == 9.9e+37: # Oscilloscope returns 9.9e+37 when no height available = 0
                heightList.append(0)
            else:
                heightList.append(float(row.strip()))
    print(heightList)
    heightList = [round(point/0.04,0) for point in heightList]
    print(heightList)
    heightCounts = Counter(heightList)
    heightCounts = dict(sorted(heightCounts.items()))
    print(heightCounts)

    poisson_lambda = 0
    i = 0
    for key in heightCounts:
        poisson_lambda += i*float(heightCounts[key])
        #print(i*float(heightCounts[key]))
        i += 1
    poisson_lambda /= len(heightList)
    print(f"Mean value of photons {poisson_lambda}")
    poisdata = np.random.poisson(poisson_lambda, 10000*len(heightList))
    length = len(heightCounts)
    labels2, counts2 = np.unique(poisdata, return_counts=True)
    counts2 = [point/10000 for point in counts2[:length]]
    labels2 = labels2[:length]
    #labels2 = [point for point in range(-1, len(labels2), 1)]
    #counts2.insert(0, 0)
    print(counts2)
    print(labels2)
    plt.bar(labels2, counts2, width = 1, edgecolor = "black", color = "orange", label = "Poissonian fit $\\mathrm{\\lambda}$="+str(poisson_lambda))
    plt.legend()

    print(heightCounts)
    plt.scatter(labels2, heightCounts.values(), marker = "s", color = "black")
    plt.show()
    
def countLEDplot(settings):
    plt.plot(LEDvolt, meanCount, marker = "s", color = "cyan")
    plt.ylabel("Mean number of photons")
    plt.xlabel("LED voltage")
    plt.savefig("./DataCollection/photonCountsLEDVolt3.72kOhm.png")
    plt.show()


if __name__ == "__main__":

    if settings["poissonParameterFit"]:
        poissonParameterFit(settings)

    if settings["plotPoissonFit"]:
        plotPoissonFit(settings)
    
    if settings["countLEDplot"]:
        countLEDplot(settings)
    
    if settings["plotPoissonHeight"]:
        plotPoissonHeight(settings)