import RPi.GPIO as GPIO
from temper import Temper
#from Clickbait import Clickbait
import time
import csv
import pymysql


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


externalTempSensor = Temper('28-011920ee9695')
beerTempSensor = Temper('28-011920e6e524')

# Place the name of the current beer here
beerName = 'Test'

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

def dbAccess(sqlData):
    #database connection
    #Creds in code boo! Do it properly or replace creds and info for your DB
    connection = pymysql.connect(host="10.0.0.69",user="the_write_user",passwd="the_password",database="beer" )
    
    #Set cursor
    cursor = connection.cursor()
    
    # Prepare the update statement
    statement = "update beers set " + sqlData + " where name = '" + beerName + "';"
    print(statement)
    #Execute statment
    cursor.execute(statement)
    #Commit the change
    connection.commit()
    
    #close the connection
    connection.close()


def main():
   
    #Define  brewing paramenters and default variables.
    targetTemp = 24
    beerTemp = 0
    ambientTemp = 0
    brewTempMax = 0
    brewTempMin = readTemps(beerTempSensor)
    heaterStatus = 0
    #Format of data is for use with chart.js to render on front end web server
    beerTempData = "{x: 0, y:" + str(readTemps(beerTempSensor)) +"}"
    ambientTempData = "{x: 0, y:" + str(readTemps(externalTempSensor)) +"}"
    #Target time in seconds
    targetTime = 7200
    actualStartTime = time.time()
    startTime = time.time()
    timeElapsed = 0
    waitTime = 3
    initTemps()
    heatOff()

    
    #While loop to control things and periodically spit out data
    while timeElapsed < targetTime:
        beerTemp = readTemps(beerTempSensor)
        print('beer temp = ' + str(beerTemp))
        ambientTemp = readTemps(externalTempSensor)
        print('External temp = ' + str(ambientTemp))
        beerTempData += ", {x: " + str(timeElapsed) + ", y: " + str(beerTemp) + "}"
        ambientTempData += ", {x: " + str(timeElapsed) + ", y: " + str(ambientTemp) + "}"
        if beerTemp > targetTemp:
            heatOff()
            heaterStatus = 0
        if beerTemp < targetTemp:
            heatOn()
            heaterStatus = 1
        if brewTempMax < beerTemp:
            brewTempMax = beerTemp
        if brewTempMin > beerTemp:
            brewTempMin = beerTemp
        #Write our data to our database
        sqlData = "brew_temp_max = '" + str(brewTempMax) + "', brew_temp_min = '" + str(brewTempMin) + "', brew_temp_now = '" + str(beerTemp) + "', brew_temp_target = '" + str(targetTemp) + "', heater_status = '" + str(heaterStatus) + "', beer_temp_data = '" + str(beerTempData) + "', ambient_temp_data = '" + str(ambientTempData) + "'"
        dbAccess(sqlData)
        time.sleep(3)
        nowTime = time.time()
        timeElapsed = round(nowTime - startTime)
        print('time elapsed = ' + str(timeElapsed))
   
    GPIO.cleanup()

main()
