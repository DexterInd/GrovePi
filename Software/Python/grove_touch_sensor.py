#!/usr/bin/env python
#
# GrovePi Example for using the Grove Touch Sensor (http://www.seeedstudio.com/wiki/Grove_-_Touch_Sensor)
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://www.dexterindustries.com/forum/?forum=grovepi
#
# LICENSE: 
# These files have been made available online through a [Creative Commons Attribution-ShareAlike 3.0](http://creativecommons.org/licenses/by-sa/3.0/) license.

import time
import grovepi

# Connect the Grove Touch Sensor to digital port D4
# SIG,NC,VCC,GND
touch_sensor = 4

grovepi.pinMode(touch_sensor,"INPUT")

while True:
    try:
        print (grovepi.digitalRead(touch_sensor))
        time.sleep(.5)

    except IOError:
        print ("Error")
