#!/usr/bin/env python
#
# GrovePi Example for using the Grove Temperature & Humidity Sensor Pro (http://www.seeedstudio.com/wiki/Grove_-_Temperature_and_Humidity_Sensor_Pro)
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://www.dexterindustries.com/forum/?forum=grovepi
#
# LICENSE: 
# These files have been made available online through a [Creative Commons Attribution-ShareAlike 3.0](http://creativecommons.org/licenses/by-sa/3.0/) license.

import grovepi

# Connect the Grove Temperature & Humidity Sensor Pro to digital port D4
# SIG,NC,VCC,GND
sensor = 4

while True:
    try:
        [temp,humidity] = grovepi.dht(sensor,1)
        print ("temp =", temp, " humidity =", humidity)

    except IOError:
        print ("Error")
