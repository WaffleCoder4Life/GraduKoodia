import matplotlib.pyplot as plt
import numpy as np


def plotData(data: list, range: float) -> plt.figure:
    """Datalista, oskilloskoopille määritetty t-akselin range mikrosekunneissa
    HUOM olettaa et eka datapiste poistettu
    -> näyttää scatter plotin datasta, t-arvot tasavälein range-alueesta
    -> palauttaa kuvaajan"""

    t = np.linspace(0, range, len(data) + 1)
    t = np.delete(t, 0)
    yticks = np.linspace(min(data), max(data), 5)

    fig = plt.figure()
    plt.yticks(yticks)
    plt.xlabel('$t$ / us')
    plt.ylabel('$U$ / V')
    plt.scatter(t, data, marker='.', c='black')
    plt.tight_layout()
    plt.show()

    return fig
