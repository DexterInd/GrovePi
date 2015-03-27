#!/usr/bin/env python
#
# GrovePi Example for using the Grove Moisture Sensor (http://www.seeedstudio.com/wiki/Grove_-_Moisture_sensor)
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://www.dexterindustries.com/forum/?forum=grovepi
#
# LICENSE: 
# These files have been made available online through a [Creative Commons Attribution-ShareAlike 3.0](http://creativecommons.org/licenses/by-sa/3.0/) license.
#
# NOTE:
# 	The wiki suggests the following sensor values:
# 		Min  Typ  Max  Condition
# 		0    0    0    sensor in open air
# 		0    20   300  sensor in dry soil
# 		300  580  700  sensor in humid soil
# 		700  940  950  sensor in water
	
# 	Sensor values observer: 
# 		Val  Condition
# 		0    sensor in open air
# 		18   sensor in dry soil
# 		425  sensor in humid soil
# 		690  sensor in water

import time
import grovepi

# Connect the Grove Moisture Sensor to analog port A0
# SIG,NC,VCC,GND
sensor = 0

while True:
    try:
        print grovepi.analogRead(sensor)
        time.sleep(.5)

    except KeyboardInterrupt:
        break
    except IOError:
        print "Error"
