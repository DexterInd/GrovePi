# tilt_buzzer.py
#
# This is an project using the Grove Switch, Buzzer and accelerometer from the GrovePi starter kit
# 
# In this project, the buzzer starts making a sound when the accelerometer is held perpendicular and the Switch is on

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