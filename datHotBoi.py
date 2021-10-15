import RPi.GPIO as GPIO
from temper import Temper
import time
import csv

###################################################################################
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
###################################################################################

# This file will read in the heating profile from a csv called 'heatProfile'
# and output to a csv called 'temperatureRecord'


#Initialise our temperature sensors with the unique IDs to address each sensor
externalTempSensor = Temper('28-011920ee9695')
beerTempSensor = Temper('28-011920e6e524')


def readTemps(sensor):
    return sensor.getTemp('C')

def initTemps():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(12, GPIO.OUT)

    #High triggers off
    GPIO.output(12, GPIO.HIGH)

def heatOn():
    #Add in a delay for safey in case of rapid switching
    time.sleep(3)
    print('HEAT ON')
    GPIO.output(12, GPIO.LOW)

def heatOff():
    #Add in a delay for safey in case of rapid switching
    time.sleep(3)
    print('HEAT OFF')
    GPIO.output(12, GPIO.HIGH)

def main():
    
    targetTemp = 24
    actualTemp = 0
    targetTime = 7200
    actualStartTime = time.time()
    startTime = time.time()
    timeElapsed = 0
    waitTime = 3
    initTemps()
    heatOff()

    
    with open('heatProfile') as csvfile:
        heatData = csv.reader(csvfile, delimiter=',')
        with open('temperatureRecord', mode='w') as csvOutFile:
            temperatureWriter = csv.writer(csvOutFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for row in heatData:
                print(row)
                startTime = time.time()
                while (time.time()-startTime) < float(row[0]):
                    if float(readTemps(beerTempSensor)) < float(row[1]):
                        print('heatOn()')
                    else:
                        print('heatOff()')
                    temperatureWriter.writerow([(time.time()-actualStartTime), readTemps(beerTempSensor), readTemps(externalTempSensor)])
                    time.sleep(waitTime) #waitTime here
        csvOutFile.close()
    csvfile.close()
    
    GPIO.cleanup()

main()
