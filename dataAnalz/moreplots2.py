import numpy as np
import time
import matplotlib.pyplot as plt
import fileHandler as fh
from readSourceMeterDataFine import readSourceMeterDataFine as read
import matplotlib.cm as cm




files = fh.ChooseFilesDifferentFolders(initdir='./dataCollection')
colors = [cm.cool(i) for i in np.linspace(0.3, 0.7, len(files))]



def main():
    for file in files:
        plt.scatter([point*1e6 for point in read(file, 0)[0:11]], [point*1e6 for point in read(file, 1)[0:11]], marker='d', label = fh.inputText("Give label for "+file), s=8, c=colors[files.index(file)])
    plt.xlabel("$I_{\\mathrm{led}}$ / $\\mu$A")
    plt.ylabel("$I_{\\mathrm{SiPM}}$ / $\\mu$A")
    plt.title("Room temp vs 1 K comparison")
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()