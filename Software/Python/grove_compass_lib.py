#!/usr/bin/env python
#
# GrovePi Library for using the Grove Compass module HCM5883 (http://www.seeedstudio.com/depot/Grove-3Axis-Digital-Compass-p-759.html)
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
# History
# ------------------------------------------------
# Author     Date      		Comments
# Karan      22 July 14  	Initial Authoring
# 	
# NOTE:		                                                              
# Refer to the datasheet to add additional functionality https://www.seeedstudio.com/wiki/images/4/42/HMC5883.pdf

import smbus
import time
import math
import RPi.GPIO as GPIO
import struct

rev = GPIO.RPI_REVISION
if rev == 2 or rev == 3:
    bus = smbus.SMBus(1)
else:
    bus = smbus.SMBus(0)
	
HMC5883L_ADDRESS            =0x1E

#CONFIGURATION_REGISTERA     =0x00
#CONFIGURATION_REGISTERB     =0x01
MODE_REGISTER               =0x02
#DATA_REGISTER_BEGIN         =0x03

#MEASUREMENT_CONTINUOUS      =0x00
#MEASUREMENT_SINGLE_SHOT     =0x01
#MEASUREMENT_IDLE            =0x03

#Do two's compiment of val (for parsing the input)
#http://stackoverflow.com/a/9147327/1945052
def twos_comp(val, bits):
	"""compute the 2's compliment of int value val"""
	if( (val&(1<<(bits-1))) != 0 ):
		val = val - (1<<bits)
	return val

#Compass class for all the values and functions
class compass:
	x=0
	y=0
	z=0
	heading=0
	headingDegrees=0
	
	def __init__(self):
		#Enable the compass
		bus.write_byte_data(HMC5883L_ADDRESS,MODE_REGISTER,0)
		time.sleep(.1)
		data=bus.read_i2c_block_data(HMC5883L_ADDRESS,0)
		compass.update(self)
	
	#Update the compass values
	def update(self):
		data=bus.read_i2c_block_data(HMC5883L_ADDRESS,0)
		compass.x=twos_comp(data[3]*256+data[4],16)
		compass.z=twos_comp(data[5]*256+data[6],16)
		compass.y=twos_comp(data[7]*256+data[8],16)
		compass.heading=math.atan2(compass.y, compass.x)
		if compass.heading <0:
			compass.heading+=2*math.pi
		if compass.heading >2*math.pi:
			compass.heading-=2*math.pi
		
		compass.headingDegrees=round(math.degrees(compass.heading),2)
		
