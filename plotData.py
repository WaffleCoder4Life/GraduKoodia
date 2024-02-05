

def plotData(data: list, points: int, range: float):
    """Datalista, datapisteitten lukumäärä, oskilloskoopille määritetty t-akselin range
    -> scatter plot datasta, t-arvot tasavälein range-alueesta"""

    plt = "matplotlib.pyplot"
    np = "numpy"
    __import__(plt)
    __import__(np)

    t = np.linspace(min(range), max(range), points)

    fig = plt.scatter(t, data, marker='s', c='mediumorchid')

    return fig

