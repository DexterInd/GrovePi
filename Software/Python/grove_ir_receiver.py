#!/usr/bin/env python
#
# GrovePi Example for using the Grove - Infrared Receiver (http://www.seeedstudio.com/depot/Grove-Infrared-Receiver-p-994.html)
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://www.dexterindustries.com/forum/?forum=grovepi
#
'''
## License
 GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
 Copyright (C) 2015  Dexter Industries

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/gpl-3.0.txt>.
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
		print (ir_data_back[1:])		#Current signal from IR remote
	time.sleep(.1)