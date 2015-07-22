# button_buzzer.py
#
# This is an project using the Grove Button, Buzzer from the GrovePi starter kit
# 
# In this project, the buzzer starts making a sound when the the button is hold

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
button = 4		#Port for Button

pinMode(buzzer_pin,"OUTPUT")	# Assign mode for buzzer as output
pinMode(button,"INPUT")		# Assign mode for Button as input
while True:
	try:
		button_status= digitalRead(button)	#Read the Button status
		if button_status:	#If the Button is in HIGH position, run the program
			digitalWrite(buzzer_pin,1)						
			# print "\tBuzzing"			
		else:		#If Button is in Off position, print "Off" on the screen
			digitalWrite(buzzer_pin,0)
			# print "Off"			
	except KeyboardInterrupt:	# Stop the buzzer before stopping
		digitalWrite(buzzer_pin,0)
		break
	except (IOError,TypeError) as e:
		print "Error"