#!/usr/bin/env python
#
# GrovePi Example for using the Grove Moisture Sensor (http://www.seeedstudio.com/wiki/Grove_-_Moisture_sensor)
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://www.dexterindustries.com/forum/?forum=grovepi
#

'''
## License
 GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
 Copyright (C) 2015  Dexter Industries

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/gpl-3.0.txt>.
'''

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
        print (grovepi.analogRead(sensor))
        time.sleep(.5)

    except KeyboardInterrupt:
        break
    except IOError:
        print ("Error")
