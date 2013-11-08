import smbus
import time
import math

bus = smbus.SMBus(1)

#I2C Address of Arduino
address = 0x04

#Command Format
dRead_cmd=[1]	#digitalRead() command format header
dWrite_cmd=[2]	#digitalWrite() command format header
aRead_cmd=[3]	#analogRead() command format header
aWrite_cmd=[4]	#analogWrite() command format header
pMode_cmd=[5]	#pinMode() command format header
uRead_cmd=[7]
acc_xyz_cmd=[20]
rtc_getTime_cmd=[30]

#Function declarations of the various functions used for encoding and sending data from RPi to Arduino
def digitalRead(pin):
	bus.write_i2c_block_data(address,1,dRead_cmd+[pin,0,0])
	time.sleep(.1)
	n=bus.read_byte(address)
	return n
	
def digitalWrite(pin,value):
	bus.write_i2c_block_data(address,1,dWrite_cmd+[pin,value,0])
	return 1
	
def pinMode(pin,mode):
	if mode == "OUTPUT":
		bus.write_i2c_block_data(address,1,pMode_cmd+[pin,1,0])
	elif mode == "INPUT":
		bus.write_i2c_block_data(address,1,pMode_cmd+[pin,0,0])
	return 1
	
def analogRead(pin):
	bus.write_i2c_block_data(address,1,aRead_cmd+[pin,0,0])
	time.sleep(.1)
	bus.read_byte(address)
	number = bus.read_i2c_block_data(address,1)
	return number[1]*256+number[2]
	
def analogWrite(pin,value):
	bus.write_i2c_block_data(address,1,aWrite_cmd+[pin,value,0])
	return 1

def temp(pin):
	a=analogRead(pin)
	resistance=(float)(1023-a)*10000/a
	t=(float)(1/(math.log(resistance/10000)/3975+1/298.15)-273.15)
	return t
	
def ultrasonicRead(pin):
	bus.write_i2c_block_data(address,1,uRead_cmd+[pin,0,0])
	time.sleep(.1)
	bus.read_byte(address)
	number = bus.read_i2c_block_data(address,1) 
	return (number[1]*256+number[2])
	
def acc_xyz():
	bus.write_i2c_block_data(address,1,acc_xyz_cmd+[0,0,0])
	time.sleep(.1)
	bus.read_byte(address)
	number = bus.read_i2c_block_data(address,1)
	if number[1]>32:
		number[1]=-(number[1]-224)
	if number[2]>32:
		number[2]=-(number[2]-224)
	if number[3]>32:
		number[3]=-(number[3]-224)
	return (number[1],number[2],number[3])

def rtc_getTime():
	bus.write_i2c_block_data(address,1,rtc_getTime_cmd+[0,0,0])
	time.sleep(.1)
	bus.read_byte(address)
	number = bus.read_i2c_block_data(address,1)
	return number