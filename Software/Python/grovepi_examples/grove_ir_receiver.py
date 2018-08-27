#!/usr/bin/env python
#
# GrovePi Example for using the Grove - Infrared Receiver (http://www.seeedstudio.com/depot/Grove-Infrared-Receiver-p-994.html)
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

# NOTE: 
#		Connect the IR sensor to any port. In the code use the pin as port+1. So if you are connecting the sensor to port 7, use "ir_recv_pin(8)"
import time
import grovepi

grovepi.ir_recv_pin(9)
print ("Press any button on the remote to see the data")
while True:
	ir_data_back=grovepi.ir_read_signal()
	if ir_data_back[0]==-1:		#IO Error
		pass
	elif ir_data_back[0]==0:	#Old signal
		pass
	else:
		print(ir_data_back[1:])		#Current signal from IR remote
	time.sleep(.1)