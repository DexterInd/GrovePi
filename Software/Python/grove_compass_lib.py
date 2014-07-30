#!/usr/bin/python
########################################################################              
# This library is for using the Grove Compass module witht he GrovePi                              
# http://www.dexterindustries.com/GrovePi/        
# Compass module: http://www.seeedstudio.com/depot/Grove-3Axis-Digital-Compass-p-759.html
#                                                       
# History
# ------------------------------------------------
# Author     Date      		Comments
# Karan      22 July 14  	Initial Authoring
# 			                                                             
# These files have been made available online through a Creative Commons Attribution-ShareAlike 3.0  license.
# (http://creativecommons.org/licenses/by-sa/3.0/)           
#
# Refer to the datasheet to add additional functionality https://www.seeedstudio.com/wiki/images/4/42/HMC5883.pdf
########################################################################
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
		
