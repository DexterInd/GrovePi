#!/usr/bin/env python
#
# GrovePi Example for using the Grove Thumb Joystick (http://www.seeedstudio.com/wiki/Grove_-_Thumb_Joystick)
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://forum.dexterindustries.com/c/grovepi
#
'''
## License

The MIT License (MIT)

GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
Copyright (C) 2015  Dexter Industries

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

import time
import grovepi

# Connect the Grove Thumb Joystick to analog port A0

# GrovePi Port A0 uses Arduino pins 0 and 1
# GrovePi Port A1 uses Arduino pins 1 and 2
# Don't plug anything into port A1 that uses pin 1
# Most Grove sensors only use 3 of their 4 pins, which is why the GrovePi shares Arduino pins between adjacent ports
# If the sensor has a pin definition SIG,NC,VCC,GND, the second (white) pin is not connected to anything

# If you wish to connect two joysticks, use ports A0 and A2 (skip A1)

# Uses two pins - one for the X axis and one for the Y axis
# This configuration means you are using port A0
xPin = 0
yPin = 1
grovepi.pinMode(xPin,"INPUT")
grovepi.pinMode(yPin,"INPUT")

# The Grove Thumb Joystick is an analog device that outputs analog signal ranging from 0 to 1023
# The X and Y axes are two ~10k potentiometers and a momentary push button which shorts the x axis

# My joystick produces slightly different results to the specifications found on the url above
# I've listed both here:

# Specifications
#     Min  Typ  Max  Click
#  X  206  516  798  1023
#  Y  203  507  797

# My Joystick
#     Min  Typ  Max  Click
#  X  253  513  766  1020-1023
#  Y  250  505  769

while True:
    try:
        # Get X/Y coordinates
        x = grovepi.analogRead(xPin)
        y = grovepi.analogRead(yPin)

        # Calculate X/Y resistance
        Rx = (float)(1023 - x) * 10 / x
        Ry = (float)(1023 - y) * 10 / y

        # Was a click detected on the X axis?
        click = 1 if x >= 1020 else 0

        print("x =", x, " y =", y, " Rx =", Rx, " Ry =", Ry, " click =", click)
        time.sleep(.5)

    except IOError:
        print ("Error")
