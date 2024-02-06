#Näyttöasetukset, Channel range 8 div, timebase range 10 div


#Laite = laitteen nimi, Voltti [V] ja time [us]
def detDisplay(laite, voltti: float, time: float)->None:
    time = str(time)
    voltti = str(voltti)
    #Set Y-axis range (bottom to top, 8 div on screen)
    laite.write(":CHANnel1:RANGe "+voltti)
    laite.write( ":TIMebase:RANGe "+time+"E-6")
