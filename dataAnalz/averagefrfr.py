import numpy as np
from array import array

def averageData(dataSetCount: int, dataSets: list) -> array:
    """Returns averaged dataset. Input: number of datasets and list of datasets to be averaged. Datasets should have eqqual number of points."""

    keys = []
    i = 0
    while i < dataSetCount:
        keys.append(str(i))
        i += 1

    sets = {}
    i = 0
    while i < len(keys):
        sets[keys[i]] = dataSets[i]
        i += 1
    
    i = 0
    average = array("f", [])
    while i < len(sets["0"]):
        av = 0
        for key in sets:
            av = av + sets[key][i]
        average.append(av / len(sets))
        i += 1
    
    return average