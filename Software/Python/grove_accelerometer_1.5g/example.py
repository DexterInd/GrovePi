#!/usr/bin/env python
#
# GrovePi Library for using the Grove - 3-Axis Digital Accelerometer(+-1.5g) v1.2b http://wiki.seeedstudio.com/wiki/Grove_-_3-Axis_Digital_Accelerometer(%C2%B11.5g)
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this library?  Ask on the forums here:  http://www.dexterindustries.com/forum/?forum=grovepi
#
# History
# ------------------------------------------------
# Author	Date      		Comments
# Shoban	19 Sep 16	  	Initial Authoring
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
from mma7660fc import MMA7660FC
import time

mma7660fc = MMA7660FC()
    
print("MMA7660FC on address 0x%x:" % (mma7660fc.address))
print("Acceleration values are in m/s^2")
while True:
	axes = mma7660fc.getAxes()
	print(( axes['x'] ),( axes['y']),( axes['z'] ))
	time.sleep(.5)
