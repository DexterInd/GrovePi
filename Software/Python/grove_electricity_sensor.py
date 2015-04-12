#!/usr/bin/env python
#
# GrovePi Example for using the Grove Electricity Sensor (http://www.seeedstudio.com/wiki/Grove_-_Electricity_Sensor)
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://www.dexterindustries.com/forum/?forum=grovepi
#
# LICENSE: 
# These files have been made available online through a [Creative Commons Attribution-ShareAlike 3.0](http://creativecommons.org/licenses/by-sa/3.0/) license.

import time
import grovepi

# Connect the Grove Electricity Sensor to analog port A0
# SIG,NC,NC,GND
sensor = 0

grovepi.pinMode(sensor,"INPUT")

# Vcc of the grove interface is normally 5v
grove_vcc = 5

while True:
    try:
        # Get sensor value
        sensor_value = grovepi.analogRead(sensor)

        # Calculate amplitude current (mA)
        amplitude_current = (float)(sensor_value / 1024 * grove_vcc / 800 * 2000000)

        # Calculate effective value (mA)
        effective_value = amplitude_current / 1.414

        # minimum_current = 1 / 1024 * grove_vcc / 800 * 2000000 / 1.414 = 8.6(mA)
        # Only for sinusoidal alternating current

        print "sensor_value", sensor_value
        print "The amplitude of the current is", amplitude_current, "mA"
        print "The effective value of the current is", effective_value, "mA"
        time.sleep(1)

    except IOError:
        print "Error"
