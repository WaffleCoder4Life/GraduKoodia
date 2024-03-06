


def readSourceMeterData(fileName: str, dataType: int)->list:
    """Reads the voltage source data from .csv file and returns a float type list. 
    dataType allowed arguments [0, 1, 2] to determine which datalist 
    is returned [Voltage, Current, Resistance]"""


    with open(fileName+".csv") as file:
        rows = []
        #File rows into a list, then delete first two rows not containing data
        for row in file:
            rows.append(row)
        del rows[2]
        del rows[1]
        del rows[0]


        #Split row into a list and add given dataType to dataList
        dataList = []
        for element in rows:
            rowAsList = element.split(",")
            dataList.append(float(rowAsList[dataType]))
        
        return dataList