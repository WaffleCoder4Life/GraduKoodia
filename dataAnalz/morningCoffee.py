import os
from datetime import date

#MAKES NEW FOLDER FOR TODAYS SHENANIGANS

def main():
    parent = "C:./dataCollection/"
    today = date.today()

    day = "{:02d}".format(today.day)
    month = "{:02d}".format(today.month)

    newFolder = day + month + str(today.year)

    print("\nGood \'morning\':)")

    pth = parent + newFolder

    if not os.path.exists(pth):
        os.makedirs(pth)

        photoPath = pth + "/Photos"
        os.makedirs(photoPath)

        tempPath = pth + "/Temp"
        os.makedirs(tempPath)
    else:
        print("File already exists!")

if __name__ == "__main__":
    main()
