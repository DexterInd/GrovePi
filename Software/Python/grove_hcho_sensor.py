#!/usr/bin/env python
#
# GrovePi Example for using the Grove HCHO Sensor (http://www.seeedstudio.com/wiki/Grove_-_HCHO_Sensor)
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://www.dexterindustries.com/forum/?forum=grovepi
#
# LICENSE: 
# These files have been made available online through a [Creative Commons Attribution-ShareAlike 3.0](http://creativecommons.org/licenses/by-sa/3.0/) license.

import time
import grovepi

# The sensitivity can be adjusted by the onboard potentiometer

# Connect the Grove HCHO Sensor to analog port A0
# SIG,NC,VCC,GND
hcho_sensor = 0

grovepi.pinMode(hcho_sensor,"INPUT")

# Vcc of the grove interface is normally 5v
grove_vcc = 5

while True:
    try:
        # Get sensor value
        sensor_value = grovepi.analogRead(hcho_sensor)

        # Calculate voltage
        voltage = (float)(sensor_value * grove_vcc / 1024)

        print "sensor_value =", sensor_value, " voltage =", voltage
        time.sleep(.5)

    except IOError:
        print "Error"
