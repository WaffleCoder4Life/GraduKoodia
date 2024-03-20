import os
from datetime import date

#MAKES NEW FOLDER FOR TODAYS SHENANIGANS

parent = "c:Documents/Tom_Sampsa/GraduKoodia/dataAnalz/dataCollection/"
today = date.today()

day = "{:02d}".format(today.day)
month = "{:02d}".format(today.month)

newFolder = day + month + str(today.year)

path = os.path.join(parent, newFolder)
os.mkdir(path)

ph = "/Photos"
photoPath = os.path.join(path, ph)
os.mkdir(photoPath)