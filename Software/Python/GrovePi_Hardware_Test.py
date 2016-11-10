#!/usr/bin/env python
#
# GrovePi Hardware Test
#	Connect Buzzer to Port D8
#	Connect Button to Analog Port A0
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.grovepi.com
#
# Have a question about this example?  Ask on the forums here:  http://forum.dexterindustries.com/c/grovepi
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
import time
import grovepi

# Connect the Grove Button to Analog Port 0.
button = 14		# This is the A0 pin.
buzzer = 8		# This is the D8 pin.

grovepi.pinMode(button,"INPUT")
grovepi.pinMode(buzzer,"OUTPUT")

print("GrovePi Basic Hardware Test.")
print("Setup:  Connect the button sensor to port A0.  Connect a Grove Buzzer to port D8.")
print("Press the button and the buzzer will buzz!")

while True:
    try:
		butt_val = grovepi.digitalRead(button)	# Each time we go through the loop, we read A0.
		print (butt_val)						# Print the value of A0.
		if butt_val == 1:
			grovepi.digitalWrite(buzzer,1)
			print ('start')
			time.sleep(1)
		else:
			grovepi.digitalWrite(buzzer,0)
			time.sleep(.5)

    except IOError:
        print ("Error")
