#!/usr/bin/env python
#
# GrovePi Example for using the Grove Chainable RGB LED (http://www.seeedstudio.com/wiki/Grove_-_Chainable_RGB_LED)
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
import chainable_rgb_direct
num_led=3

l= chainable_rgb_direct.rgb_led(num_led)

###########################
#Set Color on the first LED
#l.setColorRGB(255,0,0)

###########################
#Set color on LED chain
#RGB array needs to be sent
#r[0],g[0],b[0] specifies the color for led[0]
#r[1],g[1],b[1] specifies the color for led[1]
#r[2],g[2],b[1] specifies the color for led[2]
#Make the array length as the number of LED's 

# r=[0,0,255]
# g=[0,255,0]
# b=[255,0,0]
# l.setColorRGBs(r,g,b,num_led)

###########################
#Turn off all LED's
# r=[0,0,0]
# g=[0,0,0]
# b=[0,0,0]
# l.setColorRGBs(r,g,b,num_led)

###########################
# #Show a pattern with 3 LED's 
# while 1:
	# for i in range(0,255,5):
		# r[0]=i
		# g[0]=255-i
		# b[0]=0
		
		# r[1]=0
		# g[1]=i
		# b[1]=255-i
		
		# r[2]=255-i
		# g[2]=0
		# b[2]=i
		
		# l.setColorRGBs(r,g,b,num_led)

###########################
# Control one LED at at time 
l.setOneLED(127,127,0,0)	#Set LED 0
l.setOneLED(0,127,127,1)	#Set LED 1
l.setOneLED(0,0,0,0)		#Clear LED 0