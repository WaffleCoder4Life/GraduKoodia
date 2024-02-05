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


#EKA ALKIO KORRUPTOITUNUT -> INDEKSIT JATKOSSA 1 YLÖSPÄIN
with open("raakaData.csv", "w") as file:
    file.write(instr.read())

dataLista = []

with open("raakaData.csv") as file:
    for rivi in file:
        lista = rivi.strip().split(",")
    for alkio in lista:
        dataLista.append(alkio)

dataLista.remove(dataLista[0])
    
#print(dataLista)

dataKorjattu = []

for alkio in dataLista:
    indeksi = alkio.find("e")
    alkuOsa = float(alkio[:indeksi])
    loppuOsa = 0
    etuMerkki = ""
    indeksi2 = indeksi+2

    if alkio[indeksi+1] == "-":
        while indeksi2 < len(alkio):
        
            if alkio[indeksi2] == "0":
                indeksi2 += 1
            else:
                loppuOsa = -float(alkio[indeksi2:])
                break
    else:
        while indeksi2 < len(alkio):
        
            if alkio[indeksi2] == "0":
                indeksi2 += 1
            else:
                loppuOsa = float(alkio[indeksi2:])
                break
    
    dataKorjattu.append(alkuOsa*10**(loppuOsa))

print(dataKorjattu)
#instr.write( ":AUToscale")


