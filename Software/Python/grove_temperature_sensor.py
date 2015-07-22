#!/usr/bin/env python
#
# GrovePi Example for using the Grove Temperature Sensor (http://www.seeedstudio.com/wiki/Grove_-_Temperature_Sensor)
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
# 	The sensor uses a thermistor to detect ambient temperature.
# 	The resistance of a thermistor will increase when the ambient temperature decreases.
#	
# 	There are 3 revisions 1.0, 1.1 and 1.2, each using a different model thermistor.
# 	Each thermistor datasheet specifies a unique Nominal B-Constant which is used in the calculation forumla.
#	
# 	The second argument in the grovepi.temp() method defines which board version you have connected.
# 	Defaults to '1.0'. eg.
# 		temp = grovepi.temp(sensor)        # B value = 3975
# 		temp = grovepi.temp(sensor,'1.1')  # B value = 4250
# 		temp = grovepi.temp(sensor,'1.2')  # B value = 4250

import time
import grovepi

# Connect the Grove Temperature Sensor to analog port A0
# SIG,NC,VCC,GND
sensor = 0

while True:
    try:
        temp = grovepi.temp(sensor,'1.1')
        print ("temp =", temp)
        time.sleep(.5)

    except KeyboardInterrupt:
        break
    except IOError:
        print ("Error")
