
def readOscilloscopeData(fileName: str, dataType: int)->list:
    """Reads the oscilloscope voltage and time data from .csv file and returns a float type list. Reads file as dataCollection/'fileName'. 
    dataType allowed arguments [0, 1] to determine which datalist 
    is returned [Time, Voltage]"""


    with open("dataCollection/" + fileName + ".csv") as file:
        rows = []
        #File rows into a list, then delete first two rows not containing data
        for row in file:
            rows.append(row)
        del rows[4]
        del rows[3]
        del rows[2]
        del rows[1]
        del rows[0]


        #Split row into a list and add given dataType to dataList
        dataList = []
        for element in rows:
            rowAsList = element.split(";")
            dataList.append(float(rowAsList[dataType]))
        
        return dataList