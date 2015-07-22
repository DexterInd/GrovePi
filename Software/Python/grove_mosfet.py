#!/usr/bin/env python
#
# GrovePi Example for using the Grove MOSFET (http://www.seeedstudio.com/wiki/Grove_-_MOSFET)
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
#
# NOTE:
# 	MOSFET is also a kind of switch, but its switching frequency can reach up to 5MHz, much faster than normal mechanical relay.
# 	There are two screw terminals on opposite sides of the board.
# 	One side for power source and the other side for the device you want to control.

import time
import grovepi

# Connect the Grove MOSFET to analog port D6
# SIG,NC,VCC,GND
mosfet = 6

grovepi.pinMode(mosfet,"OUTPUT")
time.sleep(1)

while True:
    try:
        # Full speed
        grovepi.analogWrite(mosfet,255)
        print ("full speed")
        time.sleep(2)

        # Half speed
        grovepi.analogWrite(mosfet,128)
        print ("half speed")
        time.sleep(2)

        # Off
        grovepi.analogWrite(mosfet,0)
        print ("off")
        time.sleep(2)

    except KeyboardInterrupt:
        grovepi.analogWrite(mosfet,0)
        break
    except IOError:
        print ("Error")
