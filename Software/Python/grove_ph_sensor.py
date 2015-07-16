#!/usr/bin/env python
#
# GrovePi Example for using the Grove PH Sensor (http://www.seeedstudio.com/wiki/Grove_-_PH_Sensor)
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://www.dexterindustries.com/forum/?forum=grovepi
#
# LICENSE: 
# These files have been made available online through a [Creative Commons Attribution-ShareAlike 3.0](http://creativecommons.org/licenses/by-sa/3.0/) license.

import time
import grovepi

# Connect the Grove PH Sensor to analog port A0
# SIG,NC,VCC,GND
sensor = 0

grovepi.pinMode(sensor,"INPUT")
time.sleep(1)

# Reference voltage of ADC is 5v
adc_ref = 5

while True:
    try:
        # Read sensor value
        sensor_value = grovepi.analogRead(sensor)

        # Calculate PH
        ph = 7 - 1000 * (float)(sensor_value) * adc_ref / 59.16 / 1023

        print ("sensor_value =", sensor_value, " ph =", ph)

    except IOError:
        print ("Error")
