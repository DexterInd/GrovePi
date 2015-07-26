# GrovePi + Grove Ultrasonic Ranger
# http://www.seeedstudio.com/wiki/Grove_-_Ultrasonic_Ranger

# This is an project using the Grove Ultrasonic Ranger and Relay from GrovePi start kit
# 
# In this project, the ultrasonic can figure out the distance of object in front, 
# when object close to it within 10cm, the relay will turn on

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

from grovepi import *

# Connect the Grove Ultrasonic Ranger to digital port D4
# SIG,NC,VCC,GND

ultrasonic_ranger = 4
Relay_pin = 2

pinMode(Relay_pin,"OUTPUT")

while True:
    try:
		# Read distance value from Ultrasonic
		distant = ultrasonicRead(ultrasonic_ranger)
		print distant,'cm'
		if distant <= 10:
			digitalWrite(Relay_pin,1)
		else:
			digitalWrite(Relay_pin,0)

    except TypeError:
        print "Error"
    except IOError:
        print "Error"
