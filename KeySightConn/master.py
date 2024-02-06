from scipy.signal import find_peaks
import numpy as np
import matplotlib.pyplot as plt
import pyvisa as visa



def countPeaks(data: list, h: float) -> int:
    """data, peak height V -> number of peaks"""

    x = np.array(data)

    peaks, _ = find_peaks(x, height = h)

    return len(peaks)



"""Lukee datan laitteelta, muuttaa float listaksi. Mittausasetukset tulee säätää erikseen.
    Datan tulee olla ARCii -muodossa (-> mittausasetukset)"""


def readData(laite):
    with open("raakaData.csv", "w") as file:
        #Lukee laitteelta uuden datan
        file.write(laite.read())

    dataLista = []

    with open("raakaData.csv") as file:
        for rivi in file:
            lista = rivi.strip().split(",")
        for alkio in lista:
            dataLista.append(alkio)

    dataLista.remove(dataLista[0])

    return dataLista




def plotData(data: list, range: float) -> plt.figure:
    """Datalista, oskilloskoopille määritetty t-akselin range mikrosekunneissa
    HUOM olettaa et eka datapiste poistettu
    -> näyttää scatter plotin datasta, t-arvot tasavälein range-alueesta
    -> palauttaa kuvaajan"""

    t = np.linspace(0, range, len(data) + 1)
    t = np.delete(t, 0)

    fig = plt.figure()
    plt.locator_params(axis='y', nbins=5)
    plt.locator_params(axis='x', nbins=10)
    plt.xlabel('$t$ / us')
    plt.ylabel('$U$ / V')
    plt.scatter(t, data, marker='.', c='black')
    plt.tight_layout()
    plt.show()

    return fig

#Näyttöasetukset, Channel range 8 div, timebase range 10 div


#Laite = laitteen nimi, Voltti [V] ja time [us]
def setDisplay(laite, voltti: float, time: float)->None:
    time = str(time)
    voltti = str(voltti)
    #Set Y-axis range (bottom to top, 8 div on screen)
    laite.write(":CHANnel1:RANGe "+voltti)
    laite.write( ":TIMebase:RANGe "+time+"E-6")
