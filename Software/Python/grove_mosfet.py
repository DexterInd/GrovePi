#!/usr/bin/env python
#
# GrovePi Example for using the Grove MOSFET (http://www.seeedstudio.com/wiki/Grove_-_MOSFET)
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://www.dexterindustries.com/forum/?forum=grovepi
#
# LICENSE: 
# These files have been made available online through a [Creative Commons Attribution-ShareAlike 3.0](http://creativecommons.org/licenses/by-sa/3.0/) license.
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
        print "full speed"
        time.sleep(2)

        # Half speed
        grovepi.analogWrite(mosfet,128)
        print "half speed"
        time.sleep(2)

        # Off
        grovepi.analogWrite(mosfet,0)
        print "off"
        time.sleep(2)

    except KeyboardInterrupt:
        grovepi.analogWrite(mosfet,0)
        break
    except IOError:
        print "Error"
