#!/usr/bin/env python
#
# GrovePi Example for using the Grove - Infrared Receiver (http://www.seeedstudio.com/depot/Grove-Infrared-Receiver-p-994.html)
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://www.dexterindustries.com/forum/?forum=grovepi
#
# LICENSE: 
# These files have been made available online through a [Creative Commons Attribution-ShareAlike 3.0](http://creativecommons.org/licenses/by-sa/3.0/) license.

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
		print (ir_data_back[1:])		#Current signal from IR remote
	time.sleep(.1)