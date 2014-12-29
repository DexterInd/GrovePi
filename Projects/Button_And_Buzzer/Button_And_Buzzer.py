# button_buzzer.py
#
# This is an project using the Grove Button, Buzzer from the GrovePi starter kit
# 
# In this project, the buzzer starts making a sound when the the button is hold

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