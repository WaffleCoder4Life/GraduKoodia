import matplotlib.pyplot as plt
import numpy as np


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

