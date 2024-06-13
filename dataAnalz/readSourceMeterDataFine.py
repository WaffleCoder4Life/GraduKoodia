



def readSourceMeterDataFine(fileName: str, dataType: int)->list:
    """NEW VERSION: ONLY TAKES CURRENT AND SOURCE VOLTAGE.  [0, 1] -> [SOURCE VOLTAGE, CURRENT]
    
    Reads the voltage source data from .csv file and returns a float type list. 
    dataType allowed arguments [0, 1, 2, 3] to determine which datalist 
    is returned [CURRENT/RESISTANCE, TIME FROM SWITCH ON, STATUS (idk), SOURCE VOLTAGE]"""


    with open(fileName) as file:
        rows = []
        #File rows into a list, then delete first two rows not containing data
        for row in file:
            rows.append(row)
        del rows[2]
        del rows[1]
        del rows[0]

        dataList = []
        
        
        
        #Split row into a list and add given dataType to dataList
        for element in rows:
            rowAsList = element.split(",")
            dataList.append(float(rowAsList[dataType]))
        
        
        return dataList