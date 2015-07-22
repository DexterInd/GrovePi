# grovepi_lcd_dht.py
#
# This is an project for using the Grove RGB_LED Display and the Grove DHT Sensor from the GrovePi starter kit
# 
# In this project, the Temperature and humidity from the DHT sensor is printed on the RGB_LCD Display
'''
## License
 GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
 Copyright (C) 2015  Dexter Industries

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/gpl-3.0.txt>.
'''

import decimal
from grovepi import *
from grove_rgb_lcd import *

dht_sensor_port = 7     # Connect the DHt sensor to port 7
lastTemp = 0.1          # initialize a floating point temp variable
lastHum = 0.1           # initialize a floating Point humidity variable
tooLow = 62.0           # Lower limit in fahrenheit
justRight = 68.0        # Perfect Temp in fahrenheit
tooHigh = 74.0          # Temp Too high


# Function Definitions
def CtoF( tempc ):
   "This converts celcius to fahrenheit"
   tempf = round((tempc * 1.8) + 32, 2);
   return tempf;

def FtoC( tempf ):
   "This converts fahrenheit to celcius"
   tempc = round((tempf - 32) / 1.8, 2)
   return tempc;

def calcColorAdj(variance):     # Calc the adjustment value of the background color
    "Because there is 6 degrees mapping to 255 values, 42.5 is the factor for 12 degree spread"
    factor = 42.5;
    adj = abs(int(factor * variance));
    if adj > 255:
        adj = 255;
    return adj;

def calcBG(ftemp):
    "This calculates the color value for the background"
    variance = ftemp - justRight;   # Calculate the variance
    adj = calcColorAdj(variance);   # Scale it to 8 bit int
    bgList = [0,0,0]               # initialize the color array
    if(variance < 0):
        bgR = 0;                    # too cold, no red
        bgB = adj;                  # green and blue slide equally with adj
        bgG = 255 - adj;
        
    elif(variance == 0):             # perfect, all on green
        bgR = 0;
        bgB = 0;
        bgG = 255;
        
    elif(variance > 0):             #too hot - no blue
        bgB = 0;
        bgR = adj;                  # Red and Green slide equally with Adj
        bgG = 255 - adj;
        
    bgList = [bgR,bgG,bgB]          #build list of color values to return
    return bgList;

while True:

    try:
        temp = 0.01
        hum = 0.01
        [ temp,hum ] = dht(dht_sensor_port,1)       #Get the temperature and Humidity from the DHT sensor
        if (CtoF(temp) != lastTemp) and (hum != lastHum) and not math.isnan(temp) and not math.isnan(hum):
                print "lowC : ",FtoC(tooLow),"C\t\t","rightC  : ", FtoC(justRight),"C\t\t","highC : ",FtoC(tooHigh),"C" # comment these three lines
                print "lowF : ",tooLow,"F\t\tjustRight : ",justRight,"F\t\ttoHigh : ",tooHigh,"F"                       # if no monitor display
                print "tempC : ", temp, "C\t\ttempF : ",CtoF(temp),"F\t\tHumidity =", hum,"%\r\n"
                
                lastHum = hum          # save temp & humidity values so that there is no update to the RGB LCD
                ftemp = CtoF(temp)     # unless the value changes
                lastTemp = ftemp       # this reduces the flashing of the display
                # print "ftemp = ",ftemp,"  temp = ",temp   # this was just for test and debug
                
                bgList = calcBG(ftemp)           # Calculate background colors
                
                t = str(ftemp)   # "stringify" the display values
                h = str(hum)
                # print "(",bgList[0],",",bgList[1],",",bgList[2],")"   # this was to test and debug color value list
                setRGB(bgList[0],bgList[1],bgList[2])   # parse our list into the color settings
                setText("Temp:" + t + "F      " + "Humidity :" + h + "%") # update the RGB LCD display
                
    except (IOError,TypeError) as e:
        print "Error" + str(e)
    
