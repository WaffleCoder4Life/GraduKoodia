import pyvisa as visa

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
instr.write(":CHANnel1:RANGe 10")



instr.write(":ACQuire:TYPE NORMal")
instr.write(":ACQuire:COMPlete 100")
instr.write(":DIGitize CHANnel1")
instr.write(":WAVeform:SOURce CHANnel1")
instr.write( ":WAVeform:FORMat ASCii")
instr.write(":WAVeform:POINts:MODE NORMal")
instr.write( ":WAVeform:POINts 100")
instr.write( ":WAVeform:DATA?")



#instr.write( ":AUToscale")


