#!/usr/bin/env python
#
# GrovePi Example for using the Grove Piezo Vibration Sensor (http://www.seeedstudio.com/wiki/Grove-_Piezo_Vibration_Sensor)
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://www.dexterindustries.com/forum/?forum=grovepi
#
# LICENSE: 
# These files have been made available online through a [Creative Commons Attribution-ShareAlike 3.0](http://creativecommons.org/licenses/by-sa/3.0/) license.
#
# NOTE: The sensitivity can be adjusted by the onboard potentiometer

import time
import grovepi

# Connect the Grove Piezo Vibration Sensor to analog port A0
# OUT,NC,VCC,GND
piezo = 0

grovepi.pinMode(piezo,"INPUT")

while True:
    try:
        # When vibration is detected, the sensor outputs a logic high signal
        print (grovepi.analogRead(piezo))
        time.sleep(.5)

    except IOError:
        print ("Error")
