from scipy.signal import find_peaks
import numpy as np

def countPeaks(data: list, h: float):

    x = np.array(data)

    peaks, _ = find_peaks(x, height = h)

    return len(peaks)


