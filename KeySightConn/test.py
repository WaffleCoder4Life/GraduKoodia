import pyvisa as visa
import readData as gd
import countPeaks as cp
import plotData as pd

rm = visa.ResourceManager()
list = rm.list_resources()
print(list)

instr = rm.open_resource(list[0])
instr.write("*IDN?")
print(instr.read())

#Kanava 1: päällä(0/1)
instr.write("CHAN1:DISP 1")


#Label ON/OFF
#instr.write(":DISPlay:LABel OFF")

#Set probe value ??
#instr.write(":CHANnel1:PROBe 1")


#Set Y-axis range (bottom to top, 8 div on screen)
instr.write(":CHANnel1:RANGe 0.016")


singleDark = 0
crossCount = 0

i=0
while(i<10):
    #Mittausasetukset.
    instr.write(":ACQuire:TYPE NORMal")
    instr.write(":ACQuire:COMPlete 100")
    #Aseta mikä kanava käytössä
    instr.write(":DIGitize CHANnel1")
    instr.write(":WAVeform:SOURce CHANnel1")
    #Data oikeassa muodossa ASCii
    instr.write( ":WAVeform:FORMat ASCii")
    instr.write(":WAVeform:POINts:MODE NORMal")
    #Datapisteiden määrä
    instr.write( ":WAVeform:POINts 100")
    #Kysy dataa oskilloskoopilta, vain viimeinen kysely muistissa
    instr.write( ":WAVeform:DATA?")
    data = gd.readData(instr)
    i+=1
    crossCount += cp.countPeaks(data, 0)
    singleDark += cp.countPeaks(data, 0)
    


print("Cross count:",crossCount)
print("Dark count:",singleDark)


#data = gd.readData(instr)
#print(gd.readData(instr))
#pd.plotData(data, 10)



#instr.write( ":AUToscale")


