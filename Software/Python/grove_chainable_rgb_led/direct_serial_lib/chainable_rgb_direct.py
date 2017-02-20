#!/usr/bin/env python
#
# GrovePi Library for using the Grove Chainable RGB LED (http://www.seeedstudio.com/wiki/Grove_-_Chainable_RGB_LED)
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://forum.dexterindustries.com/c/grovepi
#
# Derived from the C library for the P9813 LED's by DaochenShi here: https://github.com/DC-Shi/PN532SPI-P9813GPIO
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
# Note: Connect the chainable LED to port RPISER on the GrovePi
import time,sys
import RPi.GPIO as GPIO
import smbus

class rgb_led:
	r_all=[]
	g_all=[]
	b_all=[]
	
	def __init__(self,led=1):
		GPIO.setwarnings(False)
		self.num_led=led
		self.r_all=[0] * self.num_led
		self.g_all=[0] * self.num_led
		self.b_all=[0] * self.num_led
		             
		GPIO.setmode(GPIO.BCM)  
		self.clk_pin= 15 #RX pin BCM
		self.data_pin= 14 # TX pin BCM 
		self.tv_nsec= 100
		GPIO.setup(self.clk_pin, GPIO.OUT)
		GPIO.setup(self.data_pin, GPIO.OUT)

	def sendByte(self,b):
		# print b
		for loop in range(8):
			# digitalWrite(CLKPIN, LOW);
			GPIO.output(self.clk_pin,0)
			time.sleep(self.tv_nsec/1000000.0)
			# nanosleep(&TIMCLOCKINTERVAL, NULL);
			
			# The  ic will latch a bit of data when the rising edge of the clock coming, And the data should changed after the falling edge of the clock; 
			# Copyed from P9813 datasheet
			
			if (b & 0x80) != 0:
				# digitalWrite(DATPIN, HIGH)
				GPIO.output(self.data_pin,1)
			else:
				# digitalWrite(DATPIN, LOW):
				GPIO.output(self.data_pin,0)
			
			# digitalWrite(CLKPIN, HIGH);
			GPIO.output(self.clk_pin,1)
			# nanosleep(&TIMCLOCKINTERVAL, NULL);
			time.sleep(self.tv_nsec/1000000.0)
			# //usleep(CLOCKINTERVAL);
			
			b <<= 1
			
	def sendColor(self,r, g, b):
		prefix = 0b11000000;
		if (b & 0x80) == 0:
			prefix |= 0b00100000
		if (b & 0x40) == 0:	
			prefix |= 0b00010000
		if (g & 0x80) == 0:	
			prefix |= 0b00001000
		if (g & 0x40) == 0:	
			prefix |= 0b00000100
		if (r & 0x80) == 0:	
			prefix |= 0b00000010
		if (r & 0x40) == 0:	
			prefix |= 0b00000001
	
		self.sendByte(prefix)
		self.sendByte(b)
		self.sendByte(g)
		self.sendByte(r)
		
	def setColorRGB(self,r,g,b):
		for i in range(4):
			self.sendByte(0)
		
		self.sendColor(r, g, b);
		
		for i in range(4):
			self.sendByte(0)
		
	def setColorRGBs(self,r,g,b,count):
		for i in range(4):
				self.sendByte(0)
		for i in range(count):
			self.sendColor(r[i], g[i], b[i])
		for i in range(4):
				self.sendByte(0)
	
	def setOneLED(self,r,g,b,led_num):
		self.r_all[led_num]=r
		self.g_all[led_num]=g
		self.b_all[led_num]=b
		
		self.setColorRGBs(self.r_all,self.g_all,self.b_all,self.num_led)
		
	
if __name__ == "__main__":	
	num_led=3
	
	l= rgb_led(num_led)
	
	l.setColorRGB(255,0,0)
	r=[0,0,255]
	g=[0,255,0]
	b=[255,0,0]
	l.setColorRGBs(r,g,b,num_led)