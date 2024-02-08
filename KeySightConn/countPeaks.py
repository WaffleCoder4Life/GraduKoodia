from scipy.signal import find_peaks
import numpy as np

def countPeaks(data: list, h: float, d = 5) -> int:
    """data, peak height V -> number of peaks"""

    x = np.array(data)

    peaks, _ = find_peaks(x, height = h, distance=d)

    return len(peaks)


