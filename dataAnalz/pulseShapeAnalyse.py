import readOscilloscopeData as rod
import averagefrfr as av
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import scipy.integrate as integ
from array import array
import numpy as np

settings = {
            "pathNameDate": "18032024",
            "fileName": "darkcount7K",
            "numberOfDataSets": 20,
            "backroundEnd" : 950,
            
            "averagePlotName" : "20singlecountAverage7k.png",
            "pulseAveragePlot": 1,
            "plotSinglePulse": 0
}





def plotSinglePulse(settings):
    """Use to check that pulse is in the middle"""
    plt.plot([1E6 * point for point in rod.readOscilloscopeData(settings["pathNameDate"]+"/"+settings["fileName"]+"1", 0)], [1E3 * point for point in rod.readOscilloscopeData(settings["pathNameDate"]+"/"+settings["fileName"]+"1", 1)])
    plt.xlabel("$t$ / $\\mathrm{\\mu}$s")
    plt.ylabel("$U$ / mV")
    plt.show()


def pulseAveragePlot(settings):
    #AVERAGE OF numberOfDataSets SINGLE COUNTS
    #print(list(cm._colormaps)) #LIST OF COLORMAPS :)
    fig, (ax1, ax2) = plt.subplots(2, 1)
    ax1.set_prop_cycle('color',[cm.Greens(i) for i in np.linspace(0, 1, settings["numberOfDataSets"])])


    #SAVE DATASETS FROM DARKCOUNTS TO A LIST AND CHANGES V TO mV
    #SCATTERPLOT OF ALL DATASETS WITH us TIME AXIS
    i = 1
    datasets = []
    while i <= settings["numberOfDataSets"]:
        tempor = [1E3 * point for point in rod.readOscilloscopeData(settings["pathNameDate"]+"/"+settings["fileName"]+"{0}".format(str(i)), 1)]
        #NOW [U] = mV
        datasets.append(tempor)
        ax1.plot([1E6 * point for point in rod.readOscilloscopeData(settings["pathNameDate"]+"/"+settings["fileName"]+"{0}".format(str(i)), 0)], tempor)
        i += 1

    #AVERAGE OF BACKGROUND FROM ALL DATASETS FROM START TO PULSE
    #AVERAGE OF THE AVERAGE: TO BE SUBTRACTED FROM PULSE DATA TO COMPENSATE BG
    BGaverage = av.averageData(settings["numberOfDataSets"], [dataset[:950] for dataset in datasets])


    BGcorrectiontemp = 0
    for point in BGaverage:
        BGcorrectiontemp = BGcorrectiontemp + point
    BGcorrection = BGcorrectiontemp / len(BGaverage)


    #AVERAGE PULSE DATA FROM ALL DATASETS AND SUBTRACT BG CORRECTION
    pulseaveragetemp = av.averageData(settings["numberOfDataSets"], [dataset[950:1600] for dataset in datasets])
    pulseaverage = [point - BGcorrection for point in pulseaveragetemp]
    timeAxis = [point for point in rod.readOscilloscopeData(settings["pathNameDate"]+"/"+settings["fileName"]+"1", 0)[:650]]

    #INTEGRATION USING SIMPSON'S RULE
    pulaver = np.multiply(array("f", pulseaverage),1E-3) #NOW [U] = V
    area = integ.simps(pulaver, timeAxis, dx=1, even="avg")
    areaforimage = format(area, "e")
    print(areaforimage)

    pulseCharge = format(area / (23.5*50*1.602*10**-19), "e")
    print(pulseCharge+" e")
    
    ax2.plot([1E6 * point for point in timeAxis], pulseaverage, c="black", label="Pulse\nCharge: "+pulseCharge + " e")
    ax1.set_xlabel("$t$ / $\\mathrm{\\mu}$s")
    ax1.set_ylabel("$U$ / mV")
    ax1.set_title("$R_{\\mathrm{T}}$=1.136 k$\\Omega$, SiPM bias: 24 V")
    ax2.set_xlabel("$t$ / $\\mathrm{\\mu}$s")
    ax2.set_ylabel("$U$ / mV")
    ax2.legend()
    fig.tight_layout()
    plt.savefig("./dataCollection/"+str(settings["pathNameDate"])+"/Photos/"+settings["averagePlotName"])
    plt.show()

def runAnalyze(settings):

    if settings["plotSinglePulse"]:
        plotSinglePulse(settings)

    if settings["pulseAveragePlot"]:
        pulseAveragePlot(settings)






runAnalyze(settings)