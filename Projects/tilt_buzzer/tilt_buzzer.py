# tilt_buzzer.py
#
# This is an project using the Grove Switch, Buzzer and accelerometer from the GrovePi starter kit
# 
# In this project, the buzzer starts making a sound when the accelerometer is held perpendicular and the Switch is on

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

import time
from grovepi import *
import math

buzzer_pin = 2		#Port for buzzer
switch_pin = 4		#Port for switch

pinMode(buzzer_pin,"OUTPUT")	# Assign mode for buzzer as output
pinMode(switch_pin,"INPUT")		# Assign mode for switch as input
while True:
	try:
		switch_status= digitalRead(switch_pin)	#Read the switch status
		if switch_status:	#If the switch is in HIGH position, run the program
			accl = acc_xyz()	# Get the value from the accelerometer
			print "\nX:",accl[0],"\tY:",accl[1],"\tZ:",accl[2],

			if accl[0] > 16:	# If the value on X-axis is greater than the Threshold, start the buzzer
				digitalWrite(buzzer_pin,1)
				print "\tBuzzing",			
			else:	#Else stop the buzzer
				digitalWrite(buzzer_pin,0)
		else:		#If switch is in Off position, print "Off" on the screen
			print "Off"	
		time.sleep(.1)
	except KeyboardInterrupt:	# Stop the buzzer before stopping
		digitalWrite(buzzer_pin,0)
		break
	except (IOError,TypeError) as e:
		print "Error"