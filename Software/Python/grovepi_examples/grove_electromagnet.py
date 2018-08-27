#!/usr/bin/env python
#
# GrovePi Example for using the Grove Electromagnet (http://www.seeedstudio.com/wiki/Grove_-_Electromagnet)
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://forum.dexterindustries.com/c/grovepi
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
import grovepi

# The electromagnet can hold a 1KG weight

# Connect the Grove Electromagnet to digital port D4
# SIG,NC,VCC,GND
electromagnet = 4

grovepi.pinMode(electromagnet,"OUTPUT")
time.sleep(1)

while True:
    try:
        # Switch on electromagnet
        grovepi.digitalWrite(electromagnet,1)
        print ("on")
        time.sleep(2)

        # Switch off electromagnet
        grovepi.digitalWrite(electromagnet,0)
        print ("off")
        time.sleep(2)

    except KeyboardInterrupt:
        grovepi.digitalWrite(electromagnet,0)
        break
    except IOError:
        print ("Error")
