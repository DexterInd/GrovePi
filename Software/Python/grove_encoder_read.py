#!/usr/bin/env python
#
# GrovePi Example for using the Grove Encoder(http://www.seeedstudio.com/depot/Grove-Encoder-p-1352.html) with the GrovePi
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
# Connect the grove encoder to D2 on the GrovePi.
# The encoder values go from 0 up to 32 
# (although these can be subsequently changed by utilizing a different parameter for the encoder_en function)

import time
import grovepi

print("Reading from the Grove Encoder")

# default pin is 2 and default number of steps is 32
grovepi.encoder_en()

time_to_run = 10 # 10 seconds
start = time.time() # current time in seconds
old_val = 0

while start + time_to_run > time.time():

	# defaults to pin 2
	new_val = grovepi.encoderRead()
	if old_val != new_val:
		print("{:3d}/32 position".format(new_val))
		old_val = new_val

# and disable the interrupt on pin 2
grovepi.encoder_dis()