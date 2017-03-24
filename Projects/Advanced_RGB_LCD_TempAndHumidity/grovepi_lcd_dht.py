# grovepi_lcd_dht.py
#
# This is an project for using the Grove RGB_LED Display and the Grove DHT Sensor from the GrovePi starter kit
# 
# In this project, the Temperature and humidity from the DHT sensor is printed on the RGB_LCD Display
'''
The MIT License (MIT)

GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
Copyright (C) 2017  Dexter Industries

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
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
                                                    #Change the second parameter to 0 when using DHT (instead of DHT Pro)
                                                    #You will get very large number values if you don't!
        if (CtoF(temp) != lastTemp) and (hum != lastHum) and not math.isnan(temp) and not math.isnan(hum):
                print("lowC : ",FtoC(tooLow),"C\t\t","rightC  : ", FtoC(justRight),"C\t\t","highC : ",FtoC(tooHigh),"C") # comment these three lines
                print("lowF : ",tooLow,"F\t\tjustRight : ",justRight,"F\t\ttoHigh : ",tooHigh,"F")                       # if no monitor display
                print("tempC : ", temp, "C\t\ttempF : ",CtoF(temp),"F\t\tHumidity =", hum,"%\r\n")
                
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
        print("Error" + str(e))
    
