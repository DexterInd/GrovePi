# grovepi.py
# v1.1
# This file provides the basic functions for using the GrovePi
#
# Karan Nayan
# Initial Date: 13 Feb 2014
# Last Updated: 13 Feb 2014
# http://www.dexterindustries.com/
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
################################################################################################################
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

#I2C Address of Arduino
address = 0x04

#Command Format
dRead_cmd=[1]	#digitalRead() command format header
dWrite_cmd=[2]	#digitalWrite() command format header 
aRead_cmd=[3]	#analogRead() command format header
aWrite_cmd=[4]	#analogWrite() command format header
pMode_cmd=[5]	#pinMode() command format header
uRead_cmd=[7]	#Ultrasonic read
acc_xyz_cmd=[20]	#Accelerometer (+/- 1.5g) read
rtc_getTime_cmd=[30]	#RTC get time
dht_temp_cmd=[40]	#DHT Pro sensor temperature

#Function declarations of the various functions used for encoding and sending data from RPi to Arduino

#Write I2C block
def write_i2c_block(address,block):
	try:
		return bus.write_i2c_block_data(address,1,block)
	except IOError:
		print "IOError"
		return -1

#Read I2C byte
def read_i2c_byte(address):
	try:
		return bus.read_byte(address)
	except IOError:
		print "IOError"
		return -1

#Read I2C block
def read_i2c_block(address):
	try:
		return bus.read_i2c_block_data(address,1)
	except IOError:
		print "IOError"
		return -1

#Arduino Digital Read
def digitalRead(pin):
	write_i2c_block(address,dRead_cmd+[pin,0,0])
	time.sleep(.1)
	n=read_i2c_byte(address)
	return n

#Arduino Digital Write
def digitalWrite(pin,value):
	write_i2c_block(address,dWrite_cmd+[pin,value,0])
	return 1

#Setting Up Pin mode on Arduino
def pinMode(pin,mode):
	if mode == "OUTPUT":
		write_i2c_block(address,pMode_cmd+[pin,1,0])
	elif mode == "INPUT":
		write_i2c_block(address,pMode_cmd+[pin,0,0])
	return 1

#Read analog value from Pin
def analogRead(pin):
	bus.write_i2c_block_data(address,1,aRead_cmd+[pin,0,0])
	time.sleep(.1)
	bus.read_byte(address)
	number = bus.read_i2c_block_data(address,1)
	return number[1]*256+number[2]

#Write PWM
def analogWrite(pin,value):
	write_i2c_block(address,aWrite_cmd+[pin,value,0])
	return 1

#Read temp from Grove Temp Sensor
def temp(pin):
	a=analogRead(pin)
	resistance=(float)(1023-a)*10000/a
	t=(float)(1/(math.log(resistance/10000)/3975+1/298.15)-273.15) 
	return t

#Read value from Grove Ultrasonic 
def ultrasonicRead(pin):
	write_i2c_block(address,uRead_cmd+[pin,0,0])
	time.sleep(.2)
	read_i2c_byte(address)
	number = read_i2c_block(address) 
	return (number[1]*256+number[2])

#Read Grove Accelerometer (+/- 1.5g) XYZ value
def acc_xyz():
	write_i2c_block(address,acc_xyz_cmd+[0,0,0])
	time.sleep(.1)
	read_i2c_byte(address)
	number = read_i2c_block(address)
	if number[1]>32:
		number[1]=-(number[1]-224)
	if number[2]>32:
		number[2]=-(number[2]-224)
	if number[3]>32:
		number[3]=-(number[3]-224)
	return (number[1],number[2],number[3])

#Read from Grove RTC
def rtc_getTime():
	write_i2c_block(address,rtc_getTime_cmd+[0,0,0])
	time.sleep(.1)
	read_i2c_byte(address)
	number = read_i2c_block(address)
	return number

#Read and return temperature and humidity from Grove DHT Pro
def dht(pin,module_type):
	write_i2c_block(address,dht_temp_cmd+[pin,module_type,0])

	#Delay necessary for proper reading fron DHT sensor
	time.sleep(.6) 
	try:
		read_i2c_byte(address)
		number = read_i2c_block(address)
		if number==-1:
			return -1
	except (TypeError,IndexError):
		return -1
	#data returned in IEEE format as a float in 4 bytes 
	f=0

	for element in reversed(number[1:5]):	#data is reversed 
		hex_val=hex(element)	#Converted to hex
		#print hex_val
		try:
			h_val=hex_val[2]+hex_val[3]
		except IndexError:
			h_val='0'+hex_val[2]
		if f==0:	#Convert to char array
			h=h_val
			f=1
		else:
			h=h+h_val
	t=round(struct.unpack('!f', h.decode('hex'))[0],2)#convert the temp back to float

	h=''
	for element in reversed(number[5:9]):	#data is reversed 
		hex_val=hex(element)	#Converted to hex
		#print hex_val
		try:
			h_val=hex_val[2]+hex_val[3]
		except IndexError:
			h_val='0'+hex_val[2]
		if f==0:	#Convert to char array
			h=h_val
			f=1
		else:
			h=h+h_val
	hum=round(struct.unpack('!f', h.decode('hex'))[0],2)#convert back to floatz
	t = t * 10 / 256
	hum = hum * 10 / 256
	return [t,hum]
