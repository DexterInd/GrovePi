#!/usr/bin/env python
#
# GrovePi Example for using the Grove Dust sensor(http://www.seeedstudio.com/depot/Grove-Dust-Sensor-p-1050.html) with the GrovePi
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

# USAGE
#
# Connect the dust sensor to Port D2 on the GrovePi. The dust sensor only works on that port
# The dust sensor takes 30 seconds to update the new values
#
# It returns the LPO time, the percentage (LPO time divided by total period, in this case being 30000 ms) 
# and the concentration in pcs/0.01cf

import time
import grovepi

print("Reading from the Grove Dust Sensor")

# default pin is 2 and default update period is 30000 ms
grovepi.dust_sensor_en()

time_to_run = 125 # 10 seconds
start = time.time() # current time in seconds
old_val = [0, 0.0, 0.0]

while start + time_to_run > time.time():

	# defaults to pin 2
	new_val = grovepi.dust_sensor_read()
	if old_val[0] != new_val[0]:
		print("LPO time = {:3d} | LPO% = {:5.2f} | pcs/0.01cf = {:6.1f}".format(*new_val))
		old_val = new_val

# and disable the interrupt on pin 2
grovepi.dust_sensor_dis()