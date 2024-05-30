import pyvisa as visa
from deviceControl import setDisplay, setVoltageFine, saveData
from time import sleep
import numpy as np
import matplotlib.pyplot as plt
import struct
import time
import statistics

settings = {



        # Oscilloscope display settings
        "timeRange" : 200E-9,
        "voltageRange" : 400E-3,
        "triggerLevel" : 22.5E-3, # Check before with oscilloscope, use 50 % of 1PE height, slope either

        # Main control
        "runTest" : 1,
        "plotDCR" : 0,

        # Resource control
        "closeResources" : 1,
}

# Temperature 4.00 kOhm, shutter closed, trigger level 50% of 1PE height
biasVoltage4_0kOhm = [23, 23.5, 24, 24.5, 25]
DCR4_0kOhm23 = [0.9483937606451092, 0.5964156498400349, 0.6135443213316127, 1.521805356577452, 0.9134491464379475, 0.45884118589527373, 0.7282888662194612, 0.8016527134551095, 0.4890512357147755, 0.5858912607191512, 0.5206816219451171, 0.5019775700595724, 0.48523079176099615, 0.47487996163112745, 0.41509632090506093, 0.4206009017274477, 0.46308026997357243, 0.7053537350218324, 0.5899205098530309, 0.6306835097140783]
DCR4_0kOhm23_5 = [0.8916915127757619, 0.7677549303529569, 0.6726866909592194, 0.7548926791100804, 0.6724274325709859, 0.8944874070068829, 0.7224700427939241, 0.7622460047156245, 0.6967982191450566, 0.81571864551796, 0.5381805243039113, 0.8580209944738859, 0.8777904910252273, 0.737573692279779, 0.7792920424691016, 0.49937723295899933, 0.5833468854792594, 0.6565749789589845, 0.7032799735782912, 1.0312705309873607]
DCR4_0kOhm24 = [0.9258824494647825, 1.1330363822438863, 1.0682231154978152, 0.8404322928948353, 0.8742001218834445, 1.1725832815894521, 0.9923600375960019, 0.9002798838137601, 0.8189086561150416, 1.0303665617566207, 1.4474947230897217, 0.8236512288804113, 0.8843357632315503, 1.0529516968489683, 1.0977804614017868, 1.1095637345779992, 0.9815047256067982, 0.9336838230248242, 0.8211044576344614, 0.9647002818130044]
DCR4_0kOhm24_5 = [1.9401417893003823, 1.5879300938886087, 1.4321872920126624, 1.5064422782381675, 1.5268620546673584, 1.6199786112243482, 1.3758924086244884, 2.161441809430159, 1.2093271588409504, 1.46590117463306, 1.8800848593932822, 1.7315184750320347, 1.737628837520364, 1.8470386853540541, 1.4298279052556366, 1.255978586559441, 1.7821236294649505, 1.509176987442509, 1.3910379084741198, 1.5486504282924276]
DCR4_0kOhm25V = [2.8297756396787848, 1.969858699513947, 3.834182660645425, 3.6109344725461554, 2.569292283527421, 2.6310120706584748, 1.8411471798744392, 1.9679276684351468, 2.7880882015604596, 2.7924902052629483, 2.317455832038286, 2.7156868828283267, 2.987368633345519, 1.960453162070079, 2.2626321266971057, 3.572297711858224, 2.027406257526602, 1.857325423822572, 2.396864866799616, 3.2664048017027594, 3.6207894619474765, 2.708300639953492, 2.501590298639309, 2.7692287410000644, 2.0131136186744545, 2.2673979087221308, 2.6119352864922267, 4.1056452709335645, 2.923544330810895, 2.795974352799112, 4.941973563950795, 3.333598404069287, 3.0860612876759115, 3.4845480261829693, 3.230234237585822, 2.3946682305379037, 2.444018654539082, 2.447238201636681, 2.868134510563272, 2.67148188629091, 2.35859280561248, 3.511514257191659,2.354365293388276, 3.3274076157667074, 2.9556661206688526, 2.639364805460726, 2.158252798106653, 3.5167244391291317, 2.98957907037617, 1.8635839150832403]
listOfLists = [DCR4_0kOhm23, DCR4_0kOhm23_5, DCR4_0kOhm24, DCR4_0kOhm24_5, DCR4_0kOhm25V]


# 23 mean 0.6432419344713882 with variance 0.06318493695404122
# 23.5 mean 0.7457940455731626 with variance 0.015773928267799497
# 24 mean 0.9936521839482583 with variance 0.022445952693540366
# 24.5 mean 1.5969585486824502 with variance 0.055255597025417484
# 25 mean 3.765259698538722 with variance 0.5215344099905066

if settings["plotDCR"]:
    dcrList = []
    sigmaList = []
    for list, volt in zip(listOfLists, biasVoltage4_0kOhm):
        mean = statistics.mean(list)
        variance = statistics.pvariance(list)
        print(f"{volt} mean {mean} with variance {variance}")
        dcrList.append(mean)
        sigmaList.append(np.sqrt(variance))

    fig, ax1 = plt.subplots()

    
    ax1.scatter(biasVoltage4_0kOhm, dcrList, marker = "s", s=10, c="mediumorchid", label="Dark count rate at 4.0 k$\\Omega$")
    ax1.errorbar(biasVoltage4_0kOhm, dcrList, yerr=sigmaList, fmt = "none", ecolor = "mediumorchid", capsize = 3)
    ax1.set_xlabel("Bias voltage V")
    ax1.set_ylabel("Dark count rate Hz")
    ax1.set_title("Dark count rates at 4.0 k$\\Omega$ temperature")
    plt.savefig("./DataCollection/darkcountrate4_0kOhm")
    plt.show()

if settings["runTest"]:
    #VISA CONNECTIONS
    rm = visa.ResourceManager()
    osc = rm.open_resource('USB0::0x2A8D::0x1797::CN56396144::INSTR') # Connect oscilloscope
    
    """ sour = rm.open_resource("GPIB0::22::INSTR") # Connect source
    sour.write("*RST")  # Return 6487 to GPIB defaults, USE BEFORE DISCONNECTING SIGNALS
    sour.write("SYST:ZCH OFF") # Turn off zero corrections
    sour.write(":SENS:RANG 0.00001") # SET CURRENT MEASURE RANGE (not needed but stops the device from clicking) """
    print("Resources opened")


    # Display settings for oscilloscope
    setDisplay(osc, 1, settings["voltageRange"], settings["timeRange"], settings["triggerLevel"])
    sleep(1)

    osc.write(":ACQuire:MODE SEGM") # Aquire mode segmented
    osc.write(":ACQuire:MODE?")
    print("Acquire type "+osc.read())


    segments = 50
    osc.write(":ACQuire:SEGMented:COUNt "+str(segments)) # Set amount of segments to be aquired, max 50

    darkCountRateList = []
    timeList = []
    # Runtime less than 0.1 s for trigger 0 (always triggers)
    i = 0
    while i < 20:
        sleep(0.5)
        osc.write(":SINGle")
        start = time.time()
        while True:
            sleep(0.001)
            osc.write(":WAVeform:SEGMented:COUNt?")
            dimSegments = int(osc.read().strip("\n+"))
            if dimSegments == segments:
                break

        
        end = time.time()
        measureTime = (end-start)-0.0587 # Calibrate with the average of 50 empty measurements
        timeList.append(measureTime)
        darkCountRateTemp = segments/(measureTime)
        darkCountRateList.append(darkCountRateTemp)
        print(f"{i+1} / 20 cycle completed, DCR {darkCountRateTemp}")
        i += 1
    print(timeList)
    print(darkCountRateList)
    darkCountRate = 0
    for count in darkCountRateList:
        darkCountRate += count
    darkCountRate /= len(darkCountRateList)
    print(f"Dark count rate is {darkCountRate}")


if settings["closeResources"]:
    osc.close()
    #sour.close()
    print("Resources closed")