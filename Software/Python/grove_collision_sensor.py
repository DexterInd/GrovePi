#!/usr/bin/env python
#
# GrovePi Example for using the Grove Collision Sensor (http://www.seeedstudio.com/wiki/Grove_-_Collision_Sensor)
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://www.dexterindustries.com/forum/?forum=grovepi
#
# LICENSE: 
# These files have been made available online through a [Creative Commons Attribution-ShareAlike 3.0](http://creativecommons.org/licenses/by-sa/3.0/) license.

import time
import grovepi

# Connect the Grove Collision Sensor to digital port D2
# SIG,NC,VCC,GND
collision_sensor = 2

grovepi.pinMode(collision_sensor,"INPUT")

while True:
    try:
        print (grovepi.digitalRead(collision_sensor))
        time.sleep(.5)

    except IOError:
        print ("Error")
