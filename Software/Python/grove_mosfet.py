#!/usr/bin/env python
#
# GrovePi Example for using the Grove MOSFET (http://www.seeedstudio.com/wiki/Grove_-_MOSFET)
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://forum.dexterindustries.com/c/grovepi
#
'''
## License

The MIT License (MIT)

GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
Copyright (C) 2017  Dexter Industries

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
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
