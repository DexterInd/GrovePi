#!/usr/bin/env python
#
# GrovePi Example for using the Grove Infrared Distance Interrupt (http://www.seeedstudio.com/wiki/Grove_-_IR_Distance_Interrupt)
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

# NOTE:
# The sensitivity can be adjusted by the onboard potentiometer
# Calibration
# 	Hold the sensor facing an empty dark area
# 	Adjust the potentiometer until the onboard LED switches off
# 	When the LED switches off the sensor is calibrated
# 	If not, adjust the potentiometer again

import time
import grovepi

# Connect the Grove Infrared Distance Interrupt Sensor to digital port D4
# SIG,NC,VCC,GND
sensor = 4

grovepi.pinMode(sensor,"INPUT")

while True:
    try:
        # Sensor returns LOW and onboard LED lights up when the
        # received infrared light intensity exceeds the calibrated level
        if grovepi.digitalRead(sensor) == 0:
            print ("found something")
        else:
            print ("nothing")

        time.sleep(.5)

    except IOError:
        print ("Error")
