import RPi.GPIO as GPIO
from temper import Temper
import time

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
#
###################################################################################

#Initialise our temperature sensors with the unique IDs to address them
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
    
    #targetTemp = 30
    targetTemp = 20
    actualTemp = 0
    targetTime = 864000
    startTime = time.time()
    timeElapsed = 0
    initTemps()
    heatOff()

    while timeElapsed < targetTime:
       actualTemp = readTemps(beerTempSensor)
       print('beer temp = ' + str(actualTemp))
       print('External temp = ' + str(readTemps(externalTempSensor)))
       if actualTemp > targetTemp:
           heatOff()
       if actualTemp < targetTemp:
           heatOn()
       time.sleep(30)
       nowTime = time.time()
       timeElapsed = nowTime - startTime
       print('time elapsed = ' + str(timeElapsed))

    GPIO.cleanup()

main()
GPIO.cleanup()
