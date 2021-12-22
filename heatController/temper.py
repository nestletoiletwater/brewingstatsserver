import os
import time

####################################################################################
#    License
#
#    This file is part of Brewing Stats Server.
#
#    Brewing Stats Server is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Brewing Stats Server is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Brewing Stats Server.  If not, see <https://www.gnu.org/licenses/>.
#
#    Acknowledgements
#
#    This code is based on the work of Scott Campbell of Circuit Basics.
#    Scott Campbell's code may be found here:
#    https://www.circuitbasics.com/raspberry-pi-ds18b20-temperature-sensor-tutorial/
#    
#    I make no claim of ownership over Scott Campbell's code and only used it as a
#    guide to write my own.
#
####################################################################################
 
class Temper():

     def __init__(self, id):
        
        #Initialise how to access our hardware
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

        # Read data and return in the requested units. (No Kelvin because no one brews in Kelvin)
        # fortunately the hardware chips do most of the heavy lifting and we need only grep our
        # way to victory!
    
        theData = self.readData()
        #Set a large negative value as default for debugging purposes
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
      	
