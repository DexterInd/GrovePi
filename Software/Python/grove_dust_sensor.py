#!/usr/bin/env python
#
# GrovePi Example for using the Grove Dust sensor(http://www.seeedstudio.com/depot/Grove-Dust-Sensor-p-1050.html) with the GrovePi
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://www.dexterindustries.com/forum/?forum=grovepi
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

# USAGE
#
# Connect the dust sensor to Port 8 on the GrovePi. The dust sensor only works on that port
# The dust sensor takes 30 seconds to update the new values, so you can send the 'run_in_bk=1' as a parameter to the read, e.g. grovepi.dustSensorRead(run_in_bk=1) to run the dust sensor code in the background. This basically allows the dust sensor to keep running in the background and you can read from it once every 30 seconds
#
# the fist byte is 1 for a new value and 0 for old values
# second byte is the concentration in pcs/0.01cf

import time
import grovepi

print "Reading from the dust sensor"
while True:
    try:
		[new_val,conc] = grovepi.dustSensorRead()
		if new_val:
			print conc
		time.sleep(.5) 

    except IOError:
        print ("Error")
