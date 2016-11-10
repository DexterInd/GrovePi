#!/usr/bin/env python
#
# GrovePi Example for using the Grove LED Bar (http://www.seeedstudio.com/wiki/Grove_-_LED_Bar)
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
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
import random

# Connect the Grove LED Bar to digital port D5
# DI,DCKI,VCC,GND
ledbar = 5

grovepi.pinMode(ledbar,"OUTPUT")
time.sleep(1)
i = 0

# LED Bar methods
# grovepi.ledBar_init(pin,orientation)
# grovepi.ledBar_orientation(pin,orientation)
# grovepi.ledBar_setLevel(pin,level)
# grovepi.ledBar_setLed(pin,led,state)
# grovepi.ledBar_toggleLed(pin,led)
# grovepi.ledBar_setBits(pin,state)
# grovepi.ledBar_getBits(pin)

while True:
    try:
        print ("Test 1) Initialise - red to green")
        # ledbar_init(pin,orientation)
        # orientation: (0 = red to green, 1 = green to red)
        grovepi.ledBar_init(ledbar, 0)
        time.sleep(.5)


        print ("Test 2) Set level")
        # ledbar_setLevel(pin,level)
        # level: (0-10)
        for i in range(0,11):
            grovepi.ledBar_setLevel(ledbar, i)
            time.sleep(.2)
        time.sleep(.3)

        grovepi.ledBar_setLevel(ledbar, 8)
        time.sleep(.5)

        grovepi.ledBar_setLevel(ledbar, 2)
        time.sleep(.5)

        grovepi.ledBar_setLevel(ledbar, 5)
        time.sleep(.5)


        print ("Test 3) Switch on/off a single LED")
        # ledbar_setLed(pin,led,state)
        # led: which led (1-10)
        # state: off or on (0,1)
        grovepi.ledBar_setLed(ledbar, 10, 1)
        time.sleep(.5)

        grovepi.ledBar_setLed(ledbar, 9, 1)
        time.sleep(.5)

        grovepi.ledBar_setLed(ledbar, 8, 1)
        time.sleep(.5)

        grovepi.ledBar_setLed(ledbar, 1, 0)
        time.sleep(.5)

        grovepi.ledBar_setLed(ledbar, 2, 0)
        time.sleep(.5)

        grovepi.ledBar_setLed(ledbar, 3, 0)
        time.sleep(.5)


        print ("Test 4) Toggle a single LED")
        # flip a single led - if it is currently on, it will become off and vice versa
        # ledbar_toggleLed(ledbar, led)
        grovepi.ledBar_toggleLed(ledbar, 1)
        time.sleep(.5)

        grovepi.ledBar_toggleLed(ledbar, 2)
        time.sleep(.5)

        grovepi.ledBar_toggleLed(ledbar, 9)
        time.sleep(.5)

        grovepi.ledBar_toggleLed(ledbar, 10)
        time.sleep(.5)


        print ("Test 5) Set state - control all leds with 10 bits")
        # ledbar_setBits(ledbar, state)
        # state: (0-1023) or (0x00-0x3FF) or (0b0000000000-0b1111111111) or (int('0000000000',2)-int('1111111111',2))
        for i in range(0,32):
            grovepi.ledBar_setBits(ledbar, i)
            time.sleep(.2)
        time.sleep(.3)


        print ("Test 6) Get current state")
        # state = ledbar_getBits(ledbar)
        # state: (0-1023) a bit for each of the 10 LEDs
        state = grovepi.ledBar_getBits(ledbar)
        print ("with first 5 leds lit, the state should be 31 or 0x1F")
        print (state)

        # bitwise shift five bits to the left
        state = state << 5
        # the state should now be 992 or 0x3E0
        # when saved the last 5 LEDs will be lit instead of the first 5 LEDs
        time.sleep(.5)


        print ("Test 7) Set state - save the state we just modified")
        # ledbar_setBits(ledbar, state)
        # state: (0-1023) a bit for each of the 10 LEDs
        grovepi.ledBar_setBits(ledbar, state)
        time.sleep(.5)


        print ("Test 8) Swap orientation - green to red - current state is preserved")
        # ledbar_orientation(pin,orientation)
        # orientation: (0 = red to green, 1 = green to red)
        # when you reverse the led bar orientation, all methods know how to handle the new LED index
        # green to red
        grovepi.ledBar_orientation(ledbar, 1)
        time.sleep(.5)

        # red to green
        grovepi.ledBar_orientation(ledbar, 0)
        time.sleep(.5)

        # green to red
        grovepi.ledBar_orientation(ledbar, 1)
        time.sleep(.5)


        print ("Test 9) Set level, again")
        # ledbar_setLevel(pin,level)
        # level: (0-10)
        # note the red LED is now at index 10 instead of 1
        for i in range(0,11):
            grovepi.ledBar_setLevel(ledbar, i)
            time.sleep(.2)
        time.sleep(.3)


        print ("Test 10) Set a single LED, again")
        # ledbar_setLed(pin,led,state)
        # led: which led (1-10)
        # state: off or on (0,1)
        grovepi.ledBar_setLed(ledbar, 1, 0)
        time.sleep(.5)

        grovepi.ledBar_setLed(ledbar, 3, 0)
        time.sleep(.5)

        grovepi.ledBar_setLed(ledbar, 5, 0)
        time.sleep(.5)


        print ("Test 11) Toggle a single LED, again")
        # ledbar_toggleLed(ledbar, led)
        grovepi.ledBar_toggleLed(ledbar, 2)
        time.sleep(.5)

        grovepi.ledBar_toggleLed(ledbar, 4)
        time.sleep(.5)


        print ("Test 12) Get state")
        # state = ledbar_getBits(ledbar)
        # state: (0-1023) a bit for each of the 10 LEDs
        state = grovepi.ledBar_getBits(ledbar)

        # the last 5 LEDs are lit, so the state should be 992 or 0x3E0

        # bitwise shift five bits to the right
        state = state >> 5
        # the state should now be 31 or 0x1F


        print ("Test 13) Set state, again")
        # ledbar_setBits(ledbar, state)
        # state: (0-1023) a bit for each of the 10 LEDs
        grovepi.ledBar_setBits(ledbar, state)
        time.sleep(.5)


        print ("Test 14) Step")
        # step through all 10 LEDs
        for i in range(0,11):
            grovepi.ledBar_setLevel(ledbar, i)
            time.sleep(.2)
        time.sleep(.3)


        print ("Test 15) Bounce")
        # switch on the first two LEDs
        grovepi.ledBar_setLevel(ledbar, 2)

        # get the current state (which is 0x3)
        state = grovepi.ledBar_getBits(ledbar)

        # bounce to the right
        for i in range(0,9):
            # bit shift left and update
            state <<= 1;
            grovepi.ledBar_setBits(ledbar, state)
            time.sleep(.2)

        # bounce to the left
        for i in range(0,9):
            # bit shift right and update
            state >>= 1;
            grovepi.ledBar_setBits(ledbar, state)
            time.sleep(.2)
        time.sleep(.3)


        print ("Test 16) Random")
        for i in range(0,21):
            state = random.randint(0,1023)
            grovepi.ledBar_setBits(ledbar, state)
            time.sleep(.2)
        time.sleep(.3)


        print ("Test 17) Invert")
        # set every 2nd LED on - 341 or 0x155
        state = 341
        for i in range(0,5):
            grovepi.ledBar_setBits(ledbar, state)
            time.sleep(.2)

            # bitwise XOR all 10 LEDs on with the current state
            state = 0x3FF ^ state

            grovepi.ledBar_setBits(ledbar, state)
            time.sleep(.2)
        time.sleep(.3)


        print ("Test 18) Walk through all possible combinations")
        for i in range(0,1024):
            grovepi.ledBar_setBits(ledbar, i)
            time.sleep(.1)
        time.sleep(.4)

    except KeyboardInterrupt:
        grovepi.ledBar_setBits(ledbar, 0)
        break
    except IOError:
        print ("Error")
