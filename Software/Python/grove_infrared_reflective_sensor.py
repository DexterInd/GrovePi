#!/usr/bin/env python
#
# GrovePi Example for using the Grove Infrared Reflective Sensor (http://www.seeedstudio.com/wiki/Grove_-_Infrared_Reflective_Sensor)
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://www.dexterindustries.com/forum/?forum=grovepi
#
# LICENSE: 
# These files have been made available online through a [Creative Commons Attribution-ShareAlike 3.0](http://creativecommons.org/licenses/by-sa/3.0/) license.
# 
# NOTE:
# The sensitivity can be adjusted by the onboard potentiometer
#
# Calibration
# 	Hold the sensor at the height you desire above a white surface
# 	Adjust the potentiometer until the onboard LED lights up
# 	Keep the same height and move above a black surface
# 	If the LED switches off the sensor is calibrated
# 	If not, adjust the potentiometer again

import time
import grovepi

# Connect the Grove Infrared Reflective Sensor to digital port D4
# SIG,NC,VCC,GND
sensor = 4

grovepi.pinMode(sensor,"INPUT")

while True:
    try:
        # Sensor returns HIGH on a black surface and LOW on a white surface
        if grovepi.digitalRead(sensor) == 1:
            print ("black surface detected")
        else:
            print ("white surface detected")

        time.sleep(.5)

    except IOError:
        print ("Error")
