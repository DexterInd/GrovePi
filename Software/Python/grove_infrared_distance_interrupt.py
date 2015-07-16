#!/usr/bin/env python
#
# GrovePi Example for using the Grove Infrared Distance Interrupt (http://www.seeedstudio.com/wiki/Grove_-_IR_Distance_Interrupt)
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
# Calibration
# 	Hold the sensor facing an empty dark area
# 	Adjust the potentiometer until the onboard LED switches off
# 	When the LED switches off the sensor is calibrated
# 	If not, adjust the potentiometer again

import time
import grovepi

# Connect the Grove Infrared Distance Interrupt Sensor to digital port D4
# SIG,NC,VCC,GND
sensor = 4

grovepi.pinMode(sensor,"INPUT")

while True:
    try:
        # Sensor returns LOW and onboard LED lights up when the
        # received infrared light intensity exceeds the calibrated level
        if grovepi.digitalRead(sensor) == 0:
            print ("found something")
        else:
            print ("nothing")

        time.sleep(.5)

    except IOError:
        print ("Error")
