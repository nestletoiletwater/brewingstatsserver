import os
import time
 
 
class Temper():

     def __init__(self, id):
     
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')
        self.baseDir = '/sys/bus/w1/devices/'
        self.deviceFile = self.baseDir + id + '/w1_slave'
     
     def readData(self):
        f = open(self.deviceFile, 'r')
        heatData = f.readlines()
        f.close()
        return heatData
      
     def getTemp(self, units):
        theData = self.readData()
        temp = -999.999
        while theData[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            theData = readData()
        equalsPos = theData[1].find('t=')
        if equalsPos != -1:
            tempData = theData[1][equalsPos+2:]
            if units == 'C':
                temp = float(tempData) / 1000.0
            if units == 'F':
                temp = (float(tempData) / 1000.0) * 9.0 / 5.0 + 32.0
        return temp
      	
