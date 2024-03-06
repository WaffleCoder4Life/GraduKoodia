import pyvisa as visa
import KeySightConn.setDisplay as sd
import KeySightConn.UNUSABLE.plotData as plotData
import countPeaks
import KeySightConn.setDisplay as setDisplay
import KeySightConn.generatePulses as pg
import keyboard





rm = visa.ResourceManager()
list = rm.list_resources()
print(list)

instr = rm.open_resource(list[0])
instr.write("*IDN?")
print(instr.read())

#Kanava 1: päällä(0/1)
instr.write("CHAN1:DISP 1")

setDisplay.setDisplay(instr, 0.04, 5)

instr.write(":WAVeform:SOURce CHANnel1")

instr.write( ":WAVeform:FORMat byte")

instr.write("WAVeform:POINTS 5000")

time_scale = 10**(6)*float(instr.query(":TIMebase:RANGE?"))
#print(values)
yIncrement = float(instr.query(":WAVeform:YINCREMENT?"))
yOrigin = float(instr.query("WAVeform:YORIGIN?"))
#print("Y-increment: ",yIncrement)
#print("Y-origin: ",+yOrigin)

pg.generate_pulses(instr, "800E3", "5E-3", "120E-9")

darkCounts = 0
i = 0
while(i<10):
    instr.write(":DIGitize")
    #instr.write(":WAVeform:DATA?")
    values = instr.query_binary_values(":WAVeform:DATA?", datatype = "B")
    trueValue=[]
    for value in values:
        # -128 jotta skaalaa binaarit oikein, samoin yincrement ja yorigin
        trueValue.append((value-128)*yIncrement+yOrigin)
    darkCounts += countPeaks.countPeaks(trueValue, 0.003, 500)
    i+=1

while True:
        if keyboard.is_pressed('q'):
            instr.write("WGEN:OUTPut1 0")
            print("Pulse generation stopped.")
            break 

print(darkCounts)

plotData.plotData(trueValue, time_scale)