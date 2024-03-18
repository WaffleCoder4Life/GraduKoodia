import readSourceMeterDataFine as rsf
import matplotlib.pyplot as plt

def logScatter(fileName: str, marker: str = None, markerSize: str = None, color: str = None):
    """Makes a scatter plot source meter data in a semilog scale.\n
    [I] = uA, [U] = V"""

    voltage = rsf.readSourceMeterDataFine(fileName, 0)
    current = [1E6 * point for point in rsf.readSourceMeterDataFine(fileName, 1)]

    plt.scatter(voltage, current, marker=marker, color=color, s=markerSize)