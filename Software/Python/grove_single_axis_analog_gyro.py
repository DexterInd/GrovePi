#!/usr/bin/env python
#
# GrovePi Example for using the Grove Single Axis Analog Gyro (http://www.seeedstudio.com/wiki/Grove_-_Single_Axis_Analog_Gyro)
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

# Connect the Grove Single Axis Analog Gyro to analog port A0
# SIG,NC,VCC,GND
sensor = 0

grovepi.pinMode(sensor,"INPUT")

# calibration
print ("calibrating...")
sum = 0
errors = 0
for x in range(0, 100):
    try:
        # Get sensor value
        v = grovepi.analogRead(sensor)
        sum += v
        #time.sleep(.05)
    except IOError:
        print ("Error")
        errors += 1

if errors == 100:
    print ("unable to calibrate")
    raise SystemExit

reference_value = sum / (100 - errors)

print ("finished calibrating")
print("reference_value =", reference_value)

# ready
while True:
    try:
        # Get sensor value
        sensor_value = grovepi.analogRead(sensor)

        # Calculate angular velocity (deg/s)
        velocity = ((float)(sensor_value - reference_value) * 4930.0) / 1023.0 / 0.67

        print("sensor_value =", sensor_value, " velocity =", velocity)
        time.sleep(.5)

    except IOError:
       print ("Error")
