#!/usr/bin/env python
#
# GrovePi Library for using the Grove - Barometer (High-Accuracy)(http://www.seeedstudio.com/depot/Grove-Barometer-HighAccuracy-p-1865.html
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this library?  Ask on the forums here:  http://forum.dexterindustries.com/c/grovepi
#
# This library is derived from the Arduino library written by Oliver Wang for SeeedStudio (https://github.com/Seeed-Studio/Grove_Barometer_HP20x/tree/master/HP20x_dev)
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

# use the bus that matches your raspi version
rev = GPIO.RPI_REVISION
if rev == 2 or rev == 3:
    bus = smbus.SMBus(1)
else:
    bus = smbus.SMBus(0)

class hp206c:
	address = None

	HP20X_I2C_DEV_ID       =(0xEC)>>1    #CSB PIN is VDD level(address is 0x76)
	HP20X_I2C_DEV_ID2      =(0XEE)>>1    #CSB PIN is GND level(address is 0x77)
	HP20X_SOFT_RST         =0x06
	HP20X_WR_CONVERT_CMD   =0x40
	HP20X_CONVERT_OSR4096  =0<<2
	HP20X_CONVERT_OSR2048  =1<<2
	HP20X_CONVERT_OSR1024  =2<<2
	HP20X_CONVERT_OSR512   =3<<2
	HP20X_CONVERT_OSR256   =4<<2
	HP20X_CONVERT_OSR128   =5<<2
	
	HP20X_READ_P           =0x30   #read_p command
	HP20X_READ_A           =0x31   #read_a command
	HP20X_READ_T           =0x32   #read_t command
	HP20X_READ_PT          =0x10   #read_pt command
	HP20X_READ_AT          =0x11   #read_at command
	HP20X_READ_CAL		   =0X28	  #RE-CAL ANALOG
	
	HP20X_WR_REG_MODE      =0xC0
	HP20X_RD_REG_MODE      =0x80
	
	ERR_WR_DEVID_NACK       =0x01    
	ERR_RD_DEVID_NACK       =0x02    
	ERR_WR_REGADD_NACK      =0x04   
	ERR_WR_REGCMD_NACK      =0x08   
	ERR_WR_DATA_NACK        =0x10     
	ERR_RD_DATA_MISMATCH    =0x20 
	                        
	I2C_DID_WR_MASK         =0xFE
	I2C_DID_RD_MASK         =0x01
	
	T_WIN_EN                =0X01
	PA_WIN_EN               =0X02
	T_TRAV_EN               =0X04
	PA_TRAV_EN              =0X08
	PA_RDY_EN               =0X20
	T_RDY_EN                =0X10
	                        
	T_WIN_CFG               =0X01
	PA_WIN_CFG              =0X02
	PA_MODE_P               =0X00
	PA_MODE_A               =0X40
	                        
	T_TRAV_CFG              =0X04
	                        
	OK_HP20X_DEV            =0X80		#HP20x_dev successfully initialized
	REG_PARA                =0X0F        #Status register

	OSR_CFG = HP20X_CONVERT_OSR1024
	OSR_ConvertTime = 25
	
	def __init__(self,address=0x76):
		self.address=address
		self.HP20X_IIC_WriteCmd(self.HP20X_SOFT_RST)
		time.sleep(.1)
	
	def isAvailable(self):
		return self.HP20X_IIC_ReadReg(self.REG_PARA)
		
	def ReadTemperature(self):
		self.HP20X_IIC_WriteCmd(self.HP20X_WR_CONVERT_CMD|self.OSR_CFG)
		time.sleep(self.OSR_ConvertTime/1000.0)
		t_raw = bus.read_i2c_block_data(self.address, self.HP20X_READ_T, 3)
		t=t_raw[0]<<16|t_raw[1]<<8|t_raw[2]
		if t&0x800000:
			t|=0xff000000;
		return t/100.0
	
	def ReadPressure(self):
		self.HP20X_IIC_WriteCmd(self.HP20X_WR_CONVERT_CMD|self.OSR_CFG)
		time.sleep(self.OSR_ConvertTime/1000.0)
		p_raw = bus.read_i2c_block_data(self.address, self.HP20X_READ_P, 3)
		p=p_raw[0]<<16|p_raw[1]<<8|p_raw[2]
		if p&0x800000:
			p|=0xff000000;
		return p/100.0
		
	def ReadAltitude(self):
		self.HP20X_IIC_WriteCmd(self.HP20X_WR_CONVERT_CMD|self.OSR_CFG)
		time.sleep(self.OSR_ConvertTime/1000.0)
		a_raw = bus.read_i2c_block_data(self.address, self.HP20X_READ_A, 3)
		a=a_raw[0]<<16|a_raw[1]<<8|a_raw[2]
		if a&0x800000:
			a|=0xff000000;
		return a/100.0
		
	def HP20X_IIC_WriteCmd(self,uCmd):
		bus.write_byte(self.address, uCmd)
		
	def HP20X_IIC_ReadReg(self, bReg):
		# self.HP20X_IIC_WriteCmd(bReg|self.HP20X_RD_REG_MODE)
		return bus.read_byte_data(self.address, bReg|self.HP20X_RD_REG_MODE)

if __name__ == "__main__":	
	h= hp206c()
	ret=h.isAvailable()
	if h.OK_HP20X_DEV == ret:
		print("HP20x_dev is available.")   
	else:
		print("HP20x_dev isn't available.")
		
	temp=h.ReadTemperature()
	pressure=h.ReadPressure()
	altitude=h.ReadAltitude()
	print(temp,pressure,altitude)	