#!/usr/bin/env python
#
# GrovePi example for using the Grove - 6-Axis Accelerometer&Compass v2.0(http://www.seeedstudio.com/depot/Grove-6Axis-AccelerometerCompass-v20-p-2476.html)
# 
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this library?  Ask on the forums here:  http://forum.dexterindustries.com/c/grovepi
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
import lsm303d

try:
	acc_mag=lsm303d.lsm303d()

	while True:
		
		# Get accelerometer values
		acc=acc_mag.getRealAccel()
		
		# Wait for compass to get ready
		while True:
			if acc_mag.isMagReady():
				break
				
		# Read the heading
		heading= acc_mag.getHeading()
		
		print("Acceleration of X,Y,Z is %.3fg, %.3fg, %.3fg" %(acc[0],acc[1],acc[2]))
		print("Heading %.3f degrees\n" %(heading))

except IOError:
	print("Unable to read from accelerometer, check the sensor and try again")
	