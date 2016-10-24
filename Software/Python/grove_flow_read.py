#!/usr/bin/env python
#
# GrovePi Example for using the Grove 1/4'' Flow Sensor(http://www.seeedstudio.com/depot/G14-Water-Flow-Sensor-p-1345.html) with the GrovePi
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

# USAGE
#
# Connect the Flow meter to Port 2 on the GrovePi. The flow meter only works on that port

# You can send 'run_in_bk=1' as a parameter, e.g. grovepi.flowRead(run_in_bk=1) to run the flow meter code in the background on the GrovePi. This allows you to use other functions such as digitalRead to run with the flow meter read running in the background
#
# the fist byte is 1 for a new value and 0 for old values
# second byte is flow rate in L/hour
#
# Since the flow meter uses interrupts, it is better to disable it once you are done using it
# The flow sensor readings are updated once every 2 seconds on the firmware
import time
import grovepi

import atexit
atexit.register(grovepi.flowDisable())

print("Reading from the Flow meter")
grovepi.flowEnable()
while True:
    try:
		[new_val,flow_val] = grovepi.flowRead()
		if new_val:
			print(flow_val)
		time.sleep(.5) 

    except IOError:
        print ("Error")
