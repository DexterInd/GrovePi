#!/usr/bin/env python
#
# GrovePi Example for using the analog read command to read analog sensor values
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://www.dexterindustries.com/forum/?forum=grovepi
#
# LICENSE: 
# These files have been made available online through a [Creative Commons Attribution-ShareAlike 3.0](http://creativecommons.org/licenses/by-sa/3.0/) license.
import time
import grovepi

#Sensor connected to A0 Port 
sensor = 1
grovepi.pinMode(sensor,"INPUT")
while True:
    try:
        sensor_value = grovepi.analogRead(sensor)

        print "sensor_value =", sensor_value
        time.sleep(.5)

    except IOError:
        print "Error"
