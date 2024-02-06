import master as ms

dataLista = []
with open("raakaData.csv") as file:
    for rivi in file:
        lista = rivi.strip().split(",")
    for alkio in lista:
        dataLista.append(alkio)

dataLista.remove(dataLista[0])

dataKorjattu = []

for alkio in dataLista:
    indeksi = alkio.find("e")
    alkuOsa = float(alkio[:indeksi])
    loppuOsa = 0
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


#------------------------------------------TÄHÄN ALLE TESTEJÄ TESTIDATALLA-------------------------
ms.plotData(dataKorjattu)