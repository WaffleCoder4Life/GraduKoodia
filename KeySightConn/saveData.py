import numpy as np

#Anna tiedosto muodossa data.csv
#Erottaa eri mittaukset sanalla UUSI
def saveData(instr, tiedosto: str, testinimi):
    time_scale = float(instr.query(":TIMebase:RANGE?"))
    yIncrement = float(instr.query(":WAVeform:YINCREMENT?"))
    yOrigin = float(instr.query("WAVeform:YORIGIN?"))
    dataList = []
    instr.write(":DIGitize")
    values = instr.query_binary_values(":WAVeform:DATA?", datatype = "B")
    for value in values:
        dataList.append((value-128)*yIncrement+yOrigin)
    print(len(dataList))
    time = np.linspace(0, time_scale, len(dataList))
    with open(tiedosto, "a") as file:
        i=0
        file.write(testinimi+"\n")
        while i < len(dataList):
            file.write(str(dataList[i])+";"+str(time[i])+"\n")
            i+=1
        file.write("\nUUSI\n")
