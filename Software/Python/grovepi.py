#!/usr/bin/env python
#
# GrovePi Python library
# v1.2.2
#
# This file provides the basic functions for using the GrovePi
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://www.dexterindustries.com/forum/?forum=grovepi
#
'''
## License

The MIT License (MIT)

GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
Copyright (C) 2015  Dexter Industries

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

# Karan Nayan
# Initial Date: 13 Feb 2014
# Last Updated: 01 June 2015
# http://www.dexterindustries.com/

import smbus
import time
import math
import RPi.GPIO as GPIO
import struct
import sys

debug =0

if sys.version_info<(3,0):
	p_version=2
else:
	p_version=3

rev = GPIO.RPI_REVISION
if rev == 2 or rev == 3:
	bus = smbus.SMBus(1)
else:
	bus = smbus.SMBus(0)

# I2C Address of Arduino
address = 0x04

# Command Format
# digitalRead() command format header
dRead_cmd = [1]
# digitalWrite() command format header
dWrite_cmd = [2]
# analogRead() command format header
aRead_cmd = [3]
# analogWrite() command format header
aWrite_cmd = [4]
# pinMode() command format header
pMode_cmd = [5]
# Ultrasonic read
uRead_cmd = [7]
# Get firmware version
version_cmd = [8]
# Accelerometer (+/- 1.5g) read
acc_xyz_cmd = [20]
# RTC get time
rtc_getTime_cmd = [30]
# DHT Pro sensor temperature
dht_temp_cmd = [40]

# Grove LED Bar commands
# Initialise
ledBarInit_cmd = [50]
# Set orientation
ledBarOrient_cmd = [51]
# Set level
ledBarLevel_cmd = [52]
# Set single LED
ledBarSetOne_cmd = [53]
# Toggle single LED
ledBarToggleOne_cmd = [54]
# Set all LEDs
ledBarSet_cmd = [55]
# Get current state
ledBarGet_cmd = [56]

# Grove 4 Digit Display commands
# Initialise
fourDigitInit_cmd = [70]
# Set brightness, not visible until next cmd
fourDigitBrightness_cmd = [71]
# Set numeric value without leading zeros
fourDigitValue_cmd = [72]
# Set numeric value with leading zeros
fourDigitValueZeros_cmd = [73]
# Set individual digit
fourDigitIndividualDigit_cmd = [74]
# Set individual leds of a segment
fourDigitIndividualLeds_cmd = [75]
# Set left and right values with colon
fourDigitScore_cmd = [76]
# Analog read for n seconds
fourDigitAnalogRead_cmd = [77]
# Entire display on
fourDigitAllOn_cmd = [78]
# Entire display off
fourDigitAllOff_cmd = [79]

# Grove Chainable RGB LED commands
# Store color for later use
storeColor_cmd = [90]
# Initialise
chainableRgbLedInit_cmd = [91]
# Initialise and test with a simple color
chainableRgbLedTest_cmd = [92]
# Set one or more leds to the stored color by pattern
chainableRgbLedSetPattern_cmd = [93]
# set one or more leds to the stored color by modulo
chainableRgbLedSetModulo_cmd = [94]
# sets leds similar to a bar graph, reversible
chainableRgbLedSetLevel_cmd = [95]

# Read the button from IR sensor
ir_read_cmd=[21]
# Set pin for the IR reciever
ir_recv_pin_cmd=[22]

dus_sensor_read_cmd=[10]
dust_sensor_en_cmd=[14]
dust_sensor_dis_cmd=[15]
encoder_read_cmd=[11] 
encoder_en_cmd=[16]
encoder_dis_cmd=[17]
flow_read_cmd=[12]
flow_disable_cmd=[13]
flow_en_cmd=[18]
# This allows us to be more specific about which commands contain unused bytes
unused = 0

# Function declarations of the various functions used for encoding and sending
# data from RPi to Arduino


# Write I2C block
def write_i2c_block(address, block):
	try:
		return bus.write_i2c_block_data(address, 1, block)
	except IOError:
		if debug:
			print ("IOError")
		return -1

# Read I2C byte
def read_i2c_byte(address):
	try:
		return bus.read_byte(address)
	except IOError:
		if debug:
			print ("IOError")
		return -1


# Read I2C block
def read_i2c_block(address):
	try:
		return bus.read_i2c_block_data(address, 1)
	except IOError:
		if debug:
			print ("IOError")
		return -1

# Arduino Digital Read
def digitalRead(pin):
	write_i2c_block(address, dRead_cmd + [pin, unused, unused])
	time.sleep(.1)
	n = read_i2c_byte(address)
	return n

# Arduino Digital Write
def digitalWrite(pin, value):
	write_i2c_block(address, dWrite_cmd + [pin, value, unused])
	return 1


# Setting Up Pin mode on Arduino
def pinMode(pin, mode):
	if mode == "OUTPUT":
		write_i2c_block(address, pMode_cmd + [pin, 1, unused])
	elif mode == "INPUT":
		write_i2c_block(address, pMode_cmd + [pin, 0, unused])
	return 1


# Read analog value from Pin
def analogRead(pin):
	bus.write_i2c_block_data(address, 1, aRead_cmd + [pin, unused, unused])
	time.sleep(.1)
	bus.read_byte(address)
	number = bus.read_i2c_block_data(address, 1)
	time.sleep(.1)
	return number[1] * 256 + number[2]


# Write PWM
def analogWrite(pin, value):
	write_i2c_block(address, aWrite_cmd + [pin, value, unused])
	return 1


# Read temp in Celsius from Grove Temperature Sensor
def temp(pin, model = '1.0'):
	# each of the sensor revisions use different thermistors, each with their own B value constant
	if model == '1.2':
		bValue = 4250  # sensor v1.2 uses thermistor ??? (assuming NCP18WF104F03RC until SeeedStudio clarifies)
	elif model == '1.1':
		bValue = 4250  # sensor v1.1 uses thermistor NCP18WF104F03RC
	else:
		bValue = 3975  # sensor v1.0 uses thermistor TTC3A103*39H
	a = analogRead(pin)
	resistance = (float)(1023 - a) * 10000 / a
	t = (float)(1 / (math.log(resistance / 10000) / bValue + 1 / 298.15) - 273.15)
	return t


# Read value from Grove Ultrasonic
def ultrasonicRead(pin):
	write_i2c_block(address, uRead_cmd + [pin, unused, unused])
	time.sleep(.2)
	read_i2c_byte(address)
	number = read_i2c_block(address)
	return (number[1] * 256 + number[2])


# Read the firmware version
def version():
	write_i2c_block(address, version_cmd + [unused, unused, unused])
	time.sleep(.1)
	read_i2c_byte(address)
	number = read_i2c_block(address)
	return "%s.%s.%s" % (number[1], number[2], number[3])


# Read Grove Accelerometer (+/- 1.5g) XYZ value
def acc_xyz():
	write_i2c_block(address, acc_xyz_cmd + [unused, unused, unused])
	time.sleep(.1)
	read_i2c_byte(address)
	number = read_i2c_block(address)
	if number[1] > 32:
		number[1] = - (number[1] - 224)
	if number[2] > 32:
		number[2] = - (number[2] - 224)
	if number[3] > 32:
		number[3] = - (number[3] - 224)
	return (number[1], number[2], number[3])


# Read from Grove RTC
def rtc_getTime():
	write_i2c_block(address, rtc_getTime_cmd + [unused, unused, unused])
	time.sleep(.1)
	read_i2c_byte(address)
	number = read_i2c_block(address)
	return number


# Read and return temperature and humidity from Grove DHT Pro
def dht(pin, module_type):
	write_i2c_block(address, dht_temp_cmd + [pin, module_type, unused])

	# Delay necessary for proper reading fron DHT sensor
	time.sleep(.6)
	try:
		read_i2c_byte(address)
		number = read_i2c_block(address)
		time.sleep(.1)
		if number == -1:
			return -1
	except (TypeError, IndexError):
		return -1
	# data returned in IEEE format as a float in 4 bytes
	
	if p_version==2:
		h=''
		for element in (number[1:5]):
			h+=chr(element)
			
		t_val=struct.unpack('f', h)
		t = round(t_val[0], 2)

		h = ''
		for element in (number[5:9]):
			h+=chr(element)
		
		hum_val=struct.unpack('f',h)
		hum = round(hum_val[0], 2)
	else:
		t_val=bytearray(number[1:5])
		h_val=bytearray(number[5:9])
		t=round(struct.unpack('f',t_val)[0],2)
		hum=round(struct.unpack('f',h_val)[0],2)
	return [t, hum]

# Grove LED Bar - initialise
# orientation: (0 = red to green, 1 = green to red)
def ledBar_init(pin, orientation):
	write_i2c_block(address, ledBarInit_cmd + [pin, orientation, unused])
	return 1

# Grove LED Bar - set orientation
# orientation: (0 = red to green,  1 = green to red)
def ledBar_orientation(pin, orientation):
	write_i2c_block(address, ledBarOrient_cmd + [pin, orientation, unused])
	return 1

# Grove LED Bar - set level
# level: (0-10)
def ledBar_setLevel(pin, level):
	write_i2c_block(address, ledBarLevel_cmd + [pin, level, unused])
	return 1

# Grove LED Bar - set single led
# led: which led (1-10)
# state: off or on (0-1)
def ledBar_setLed(pin, led, state):
	write_i2c_block(address, ledBarSetOne_cmd + [pin, led, state])
	return 1

# Grove LED Bar - toggle single led
# led: which led (1-10)
def ledBar_toggleLed(pin, led):
	write_i2c_block(address, ledBarToggleOne_cmd + [pin, led, unused])
	return 1

# Grove LED Bar - set all leds
# state: (0-1023) or (0x00-0x3FF) or (0b0000000000-0b1111111111) or (int('0000000000',2)-int('1111111111',2))
def ledBar_setBits(pin, state):
	byte1 = state & 255
	byte2 = state >> 8
	write_i2c_block(address, ledBarSet_cmd + [pin, byte1, byte2])
	return 1

# Grove LED Bar - get current state
# state: (0-1023) a bit for each of the 10 LEDs
def ledBar_getBits(pin):
	write_i2c_block(address, ledBarGet_cmd + [pin, unused, unused])
	time.sleep(.2)
	read_i2c_byte(0x04)
	block = read_i2c_block(0x04)
	return block[1] ^ (block[2] << 8)


# Grove 4 Digit Display - initialise
def fourDigit_init(pin):
	write_i2c_block(address, fourDigitInit_cmd + [pin, unused, unused])
	return 1

# Grove 4 Digit Display - set numeric value with or without leading zeros
# value: (0-65535) or (0000-FFFF)
def fourDigit_number(pin, value, leading_zero):
	# split the value into two bytes so we can render 0000-FFFF on the display
	byte1 = value & 255
	byte2 = value >> 8
	# separate commands to overcome current 4 bytes per command limitation
	if (leading_zero):
		write_i2c_block(address, fourDigitValue_cmd + [pin, byte1, byte2])
	else:
		write_i2c_block(address, fourDigitValueZeros_cmd + [pin, byte1, byte2])
	time.sleep(.05)
	return 1

# Grove 4 Digit Display - set brightness
# brightness: (0-7)
def fourDigit_brightness(pin, brightness):
	# not actually visible until next command is executed
	write_i2c_block(address, fourDigitBrightness_cmd + [pin, brightness, unused])
	time.sleep(.05)
	return 1

# Grove 4 Digit Display - set individual segment (0-9,A-F)
# segment: (0-3)
# value: (0-15) or (0-F)
def fourDigit_digit(pin, segment, value):
	write_i2c_block(address, fourDigitIndividualDigit_cmd + [pin, segment, value])
	time.sleep(.05)
	return 1

# Grove 4 Digit Display - set 7 individual leds of a segment
# segment: (0-3)
# leds: (0-255) or (0-0xFF) one bit per led, segment 2 is special, 8th bit is the colon
def fourDigit_segment(pin, segment, leds):
	write_i2c_block(address, fourDigitIndividualLeds_cmd + [pin, segment, leds])
	time.sleep(.05)
	return 1

# Grove 4 Digit Display - set left and right values (0-99), with leading zeros and a colon
# left: (0-255) or (0-FF)
# right: (0-255) or (0-FF)
# colon will be lit
def fourDigit_score(pin, left, right):
	write_i2c_block(address, fourDigitScore_cmd + [pin, left, right])
	time.sleep(.05)
	return 1

# Grove 4 Digit Display - display analogRead value for n seconds, 4 samples per second
# analog: analog pin to read
# duration: analog read for this many seconds
def fourDigit_monitor(pin, analog, duration):
	write_i2c_block(address, fourDigitAnalogRead_cmd + [pin, analog, duration])
	time.sleep(duration + .05)
	return 1

# Grove 4 Digit Display - turn entire display on (88:88)
def fourDigit_on(pin):
	write_i2c_block(address, fourDigitAllOn_cmd + [pin, unused, unused])
	time.sleep(.05)
	return 1

# Grove 4 Digit Display - turn entire display off
def fourDigit_off(pin):
	write_i2c_block(address, fourDigitAllOff_cmd + [pin, unused, unused])
	time.sleep(.05)
	return 1

# Grove Chainable RGB LED - store a color for later use
# red: 0-255
# green: 0-255
# blue: 0-255
def storeColor(red, green, blue):
	write_i2c_block(address, storeColor_cmd + [red, green, blue])
	time.sleep(.05)
	return 1

# Grove Chainable RGB LED - initialise
# numLeds: how many leds do you have in the chain
def chainableRgbLed_init(pin, numLeds):
	write_i2c_block(address, chainableRgbLedInit_cmd + [pin, numLeds, unused])
	time.sleep(.05)
	return 1

# Grove Chainable RGB LED - initialise and test with a simple color
# numLeds: how many leds do you have in the chain
# testColor: (0-7) 3 bits in total - a bit for red, green and blue, eg. 0x04 == 0b100 (0bRGB) == rgb(255, 0, 0) == #FF0000 == red
#            ie. 0 black, 1 blue, 2 green, 3 cyan, 4 red, 5 magenta, 6 yellow, 7 white
def chainableRgbLed_test(pin, numLeds, testColor):
	write_i2c_block(address, chainableRgbLedTest_cmd + [pin, numLeds, testColor])
	time.sleep(.05)
	return 1

# Grove Chainable RGB LED - set one or more leds to the stored color by pattern
# pattern: (0-3) 0 = this led only, 1 all leds except this led, 2 this led and all leds inwards, 3 this led and all leds outwards
# whichLed: index of led you wish to set counting outwards from the GrovePi, 0 = led closest to the GrovePi
def chainableRgbLed_pattern(pin, pattern, whichLed):
	write_i2c_block(address, chainableRgbLedSetPattern_cmd + [pin, pattern, whichLed])
	time.sleep(.05)
	return 1

# Grove Chainable RGB LED - set one or more leds to the stored color by modulo
# offset: index of led you wish to start at, 0 = led closest to the GrovePi, counting outwards
# divisor: when 1 (default) sets stored color on all leds >= offset, when 2 sets every 2nd led >= offset and so on
def chainableRgbLed_modulo(pin, offset, divisor):
	write_i2c_block(address, chainableRgbLedSetModulo_cmd + [pin, offset, divisor])
	time.sleep(.05)
	return 1

# Grove Chainable RGB LED - sets leds similar to a bar graph, reversible
# level: (0-10) the number of leds you wish to set to the stored color
# reversible (0-1) when 0 counting outwards from GrovePi, 0 = led closest to the GrovePi, otherwise counting inwards
def chainableRgbLed_setLevel(pin, level, reverse):
	write_i2c_block(address, chainableRgbLedSetLevel_cmd + [pin, level, reverse])
	time.sleep(.05)
	return 1

# Grove - Infrared Receiver- get the commands received from the Grove IR sensor
def ir_read_signal():
	try:
		write_i2c_block(address,ir_read_cmd+[unused,unused,unused])
		time.sleep(.1)
		data_back= bus.read_i2c_block_data(address, 1)[0:21]
		if (data_back[1]!=255):
			return data_back
		return [-1]*21
	except IOError:
		return [-1]*21
		
# Grove - Infrared Receiver- set the pin on which the Grove IR sensor is connected
def ir_recv_pin(pin):
	write_i2c_block(address,ir_recv_pin_cmd+[pin,unused,unused])
	
def dust_sensor_en():
	write_i2c_block(address, dust_sensor_en_cmd + [unused, unused, unused])
	time.sleep(.2)
	
def dust_sensor_dis():
	write_i2c_block(address, dust_sensor_dis_cmd + [unused, unused, unused])
	time.sleep(.2)
	
def dustSensorRead():
	write_i2c_block(address, dus_sensor_read_cmd + [unused, unused, unused])
	time.sleep(.2)
	#read_i2c_byte(address)
	#number = read_i2c_block(address)
	#return (number[1] * 256 + number[2])
	data_back= bus.read_i2c_block_data(address, 1)[0:4]
	#print data_back[:4]
	if data_back[0]!=255:
		lowpulseoccupancy=(data_back[3]*256*256+data_back[2]*256+data_back[1])
		#print [data_back[0],lowpulseoccupancy]
		return [data_back[0],lowpulseoccupancy]
	else:
		return [-1,-1]
	print data_back
	
def encoder_en():
	write_i2c_block(address, encoder_en_cmd + [unused, unused, unused])
	time.sleep(.2)
	
def encoder_dis():
	write_i2c_block(address, encoder_dis_cmd + [unused, unused, unused])
	time.sleep(.2)
	
def encoderRead():
	write_i2c_block(address, encoder_read_cmd + [unused, unused, unused])
	time.sleep(.2)
	data_back= bus.read_i2c_block_data(address, 1)[0:2]
	#print data_back
	if data_back[0]!=255:
		return [data_back[0],data_back[1]]
	else:
		return [-1,-1]
		
def flowDisable():
	write_i2c_block(address, flow_disable_cmd + [unused, unused, unused])
	time.sleep(.2)
	
def flowEnable():
	write_i2c_block(address, flow_en_cmd + [unused, unused, unused])
	time.sleep(.2)
	
def flowRead():
	write_i2c_block(address, flow_read_cmd + [unused, unused, unused])
	time.sleep(.2)
	data_back= bus.read_i2c_block_data(address, 1)[0:3]
	#print data_back
	if data_back[0]!=255:
		return [data_back[0],data_back[2]*256+data_back[1]]
	else:
		return [-1,-1]