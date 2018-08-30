#!/usr/bin/env python
#
# GrovePi Library for using the Grove - 6-Axis Accelerometer&Compass v2.0(http://www.seeedstudio.com/depot/Grove-6Axis-AccelerometerCompass-v20-p-2476.html)
#
# This sensor uses LSM303D chip and the library works in Python for the Raspberry Pi
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this library?  Ask on the forums here:  http://forum.dexterindustries.com/c/grovepi
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

import time,sys
import RPi.GPIO as GPIO
import smbus
import math

# use the bus that matches your raspi version
rev = GPIO.RPI_REVISION
if rev == 2 or rev == 3:
    bus = smbus.SMBus(1)
else:
    bus = smbus.SMBus(0)

class lsm303d:
	# LSM303 Address definitions 
	LSM303D_ADDR	= 0x1E  # assuming SA0 grounded

	# LSM303 Register definitions 
	TEMP_OUT_L		= 0x05
	TEMP_OUT_H		= 0x06
	STATUS_REG_M	= 0x07
	OUT_X_L_M 		= 0x08
	OUT_X_H_M 		= 0x09
	OUT_Y_L_M 		= 0x0A
	OUT_Y_H_M 		= 0x0B
	OUT_Z_L_M 		= 0x0C
	OUT_Z_H_M 		= 0x0D
	WHO_AM_I		= 0x0F
	INT_CTRL_M		= 0x12
	INT_SRC_M		= 0x13
	INT_THS_L_M		= 0x14
	INT_THS_H_M		= 0x15
	OFFSET_X_L_M	= 0x16
	OFFSET_X_H_M	= 0x17
	OFFSET_Y_L_M	= 0x18
	OFFSET_Y_H_M	= 0x19
	OFFSET_Z_L_M	= 0x1A
	OFFSET_Z_H_M	= 0x1B
	REFERENCE_X 	= 0x1C
	REFERENCE_Y 	= 0x1D
	REFERENCE_Z 	= 0x1E
	CTRL_REG0 		= 0x1F
	CTRL_REG1 		= 0x20
	CTRL_REG2		= 0x21
	CTRL_REG3 		= 0x22
	CTRL_REG4 		= 0x23
	CTRL_REG5 		= 0x24
	CTRL_REG6 		= 0x25
	CTRL_REG7 		= 0x26
	STATUS_REG_A	= 0x27
	OUT_X_L_A 		= 0x28
	OUT_X_H_A 		= 0x29
	OUT_Y_L_A 		= 0x2A
	OUT_Y_H_A 		= 0x2B
	OUT_Z_L_A 		= 0x2C
	OUT_Z_H_A 		= 0x2D
	FIFO_CTRL		= 0x2E
	FIFO_SRC		= 0x2F
	IG_CFG1			= 0x30
	IG_SRC1			= 0x31
	IG_THS1			= 0x32
	IG_DUR1			= 0x33
	IG_CFG2			= 0x34
	IG_SRC2			= 0x35
	IG_THS2			= 0x36
	IG_DUR2			= 0x37
	CLICK_CFG		= 0x38
	CLICK_SRC		= 0x39
	CLICK_THS		= 0x3A
	TIME_LIMIT		= 0x3B
	TIME_LATENCY	= 0x3C
	TIME_WINDOW		= 0x3D
	ACT_THS			= 0x3E
	ACT_DUR			= 0x3F

	MAG_SCALE_2 	= 0x00 #full-scale is +/-2Gauss
	MAG_SCALE_4 	= 0x20 #+/-4Gauss
	MAG_SCALE_8 	= 0x40 #+/-8Gauss
	MAG_SCALE_12 	= 0x60 #+/-12Gauss

	ACCELE_SCALE 	= 2
	
	X 				= 0
	Y 				= 1
	Z 				= 2
	
	# Set up the sensor
	def __init__(self,):
		self.write_reg(0x57, self.CTRL_REG1)				# 0x57 = ODR=50hz, all accel axes on
		self.write_reg((3<<6)|(0<<3), self.CTRL_REG2)  	# set full-scale
		self.write_reg(0x00, self.CTRL_REG3)  			# no interrupt
		self.write_reg(0x00, self.CTRL_REG4)  			# no interrupt
		self.write_reg((4<<2), self.CTRL_REG5)  			# 0x10 = mag 50Hz output rate
		self.write_reg(self.MAG_SCALE_2, self.CTRL_REG6)		# magnetic scale = +/-1.3Gauss
		self.write_reg(0x00, self.CTRL_REG7)  			# 0x00 = continouous conversion mode
		time.sleep(.005)
	
	# get the status of the sensor
	def status(self):
		if self.read_reg(self.WHO_AM_I) !=73:
			return -1
		return 1
		
	# Write data to a reg on the I2C device
	def write_reg(self,data,reg):
		bus.write_byte_data(self.LSM303D_ADDR, reg, data)
		
	# Read data from the sensor
	def read_reg(self,reg):
		return bus.read_byte_data(self.LSM303D_ADDR, reg)
		
	# Check if compass is ready
	def isMagReady(self):
		if self.read_reg(self.STATUS_REG_M)&0x03!=0:
			return 1
		return 0

	# Get raw accelerometer values	
	def getAccel(self):
		raw_accel=[0,0,0]
		raw_accel[0]=((self.read_reg(self.OUT_X_H_A)<<8)|self.read_reg(self.OUT_X_L_A))
		raw_accel[1]=((self.read_reg(self.OUT_Y_H_A)<<8)|self.read_reg(self.OUT_Y_L_A))
		raw_accel[2]=((self.read_reg(self.OUT_Z_H_A)<<8)|self.read_reg(self.OUT_Z_L_A))
		
		#2's compiment
		for i in range(3):
			if raw_accel[i]>32767:
				raw_accel[i]=raw_accel[i]-65536
				
		return raw_accel
	
	# Get accelerometer values in g
	def getRealAccel(self):
		realAccel=[0.0,0.0,0.0]
		accel=self.getAccel()
		for i in range(3):
			realAccel[i] = round(accel[i] / math.pow(2, 15) * self.ACCELE_SCALE,3)
		return realAccel
			
	# Get compass raw values
	def getMag(self):
		raw_mag=[0,0,0]
		raw_mag[0]=(self.read_reg(self.OUT_X_H_M)<<8)|self.read_reg(self.OUT_X_L_M)
		raw_mag[1]=(self.read_reg(self.OUT_Y_H_M)<<8)|self.read_reg(self.OUT_Y_L_M)
		raw_mag[2]=(self.read_reg(self.OUT_Z_H_M)<<8)|self.read_reg(self.OUT_Z_L_M)
		
		#2's compiment
		for i in range(3):
			if raw_mag[i]>32767:
				raw_mag[i]=raw_mag[i]-65536
				
		return raw_mag
		
	# Get heading from the compass
	def getHeading(self):
		magValue=self.getMag()
		heading = 180*math.atan2(magValue[self.Y], magValue[self.X])/math.pi#  // assume pitch, roll are 0

		if (heading <0):
			heading += 360

		return round(heading,3)
		
	def getTiltHeading(self):
		magValue=self.getMag()
		accelValue=self.getRealAccel()
		
		X=self.X
		Y=self.Y
		Z=self.Z
		
		pitch = math.asin(-accelValue[X])
		
		print(accelValue[Y],pitch,math.cos(pitch),accelValue[Y]/math.cos(pitch),math.asin(accelValue[Y]/math.cos(pitch)))
		roll = math.asin(accelValue[Y]/math.cos(pitch))

		xh = magValue[X] * math.cos(pitch) + magValue[Z] * math.sin(pitch)
		yh = magValue[X] * math.sin(roll) * math.sin(pitch) + magValue[Y] * math.cos(roll) - magValue[Z] * math.sin(roll) * math.cos(pitch)
		zh = -magValue[X] * (roll) * math.sin(pitch) + magValue[Y] * math.sin(roll) + magValue[Z] * math.cos(roll) * math.cos(pitch)
		heading = 180 * math.atan2(yh, xh)/math.pi

		if (yh >= 0):
			return heading
		else:
			return (360 + heading)
			
if __name__ == "__main__":		
	acc_mag=lsm303d()
	while True:
		print(acc_mag.getRealAccel())
		
		while True:
			if acc_mag.isMagReady():
				break
		print(acc_mag.getHeading())
		
		# Do not use, math error
		# print acc_mag.getTiltHeading()
	