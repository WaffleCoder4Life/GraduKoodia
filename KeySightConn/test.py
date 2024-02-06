import pyvisa as visa
import master as ms

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


ms.setDisplay(instr, 0.04, 5)
#Mittausasetukset.
instr.write(":ACQuire:TYPE NORMal")
instr.write(":ACQuire:COMPlete 100")
instr.write(":WAVeform:SOURce CHANnel1")
#Data oikeassa muodossa ASCii
instr.write( ":WAVeform:FORMat ASCii")
instr.write(":WAVeform:POINts:MODE NORMal")
#Datapisteiden määrä
instr.write( ":WAVeform:POINts 1000")

singleDark = 0
crossCount = 0

i=0
while(i<10):
    #Lähettää capture komennon kanavalle1, asetukset capturelle määritetään AQUire subsysteemillä
    instr.write(":DIGitize CHANnel1")
    #Kysy dataa oskilloskoopilta, vain viimeinen kysely muistissa
    #Asetukset mitä kysytään aiemmillla WAVeform komennoilla
    instr.write( ":WAVeform:DATA?")
    data = ms.readData(instr)
    i+=1
    crossCount += ms.countPeaks(data, 0.005)
    singleDark += ms.countPeaks(data, 0.005)
    

print("Cross count:",crossCount)
print("Dark count:",singleDark)

#data = ms.readData(instr)

#data = ms.readData(instr)
#print(ms.readData(instr))
#ms.plotData(data, 10)



#instr.write( ":AUToscale")


