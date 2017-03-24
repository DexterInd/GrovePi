#!/usr/bin/env python

# GrovePi LED blink test for the Grove LED Socket (http://www.seeedstudio.com/wiki/Grove_-_LED_Socket_Kit)
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://www.dexterindustries.com/forum/?forum=grovepi
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

import time
from grovepi import *

# Connect the Grove LED to digital port D4,D5,D6
led0 = 4
led1 = 5
led2 = 6

pinMode(led0,"OUTPUT")
pinMode(led1,"OUTPUT")
pinMode(led2,"OUTPUT")

while True:
    try:
        #Blink the LED
        digitalWrite(led0,1)		# Send HIGH to switch on LED
        digitalWrite(led1,1)		# Send HIGH to switch on LED
        digitalWrite(led2,1)		# Send HIGH to switch on LED
        print ("LED ON!")
        time.sleep(1)

        digitalWrite(led0,0)		# Send LOW to switch off LED
        digitalWrite(led1,0)		# Send LOW to switch off LED
        digitalWrite(led2,0)		# Send LOW to switch off LED
        print ("LED OFF!")
        time.sleep(1)

    except IOError:				# Print "Error" if communication error encountered
        print ("Error")
