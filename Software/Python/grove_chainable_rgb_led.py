#!/usr/bin/env python
#
# GrovePi Example for using the Grove Chainable RGB LED (http://www.seeedstudio.com/wiki/Grove_-_Chainable_RGB_LED)
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

# Connect first LED in Chainable RGB LED chain to digital port D7
# In: CI,DI,VCC,GND
# Out: CO,DO,VCC,GND
pin = 7

# I have 10 LEDs connected in series with the first connected to the GrovePi and the last not connected
# First LED input socket connected to GrovePi, output socket connected to second LED input and so on
numleds = 10     #If you only plug 1 LED, change 10 to 1

grovepi.pinMode(pin,"OUTPUT")
time.sleep(1)

# Chainable RGB LED methods
# grovepi.storeColor(red, green, blue)
# grovepi.chainableRgbLed_init(pin, numLeds)
# grovepi.chainableRgbLed_test(pin, numLeds, testColor)
# grovepi.chainableRgbLed_pattern(pin, pattern, whichLed)
# grovepi.chainableRgbLed_modulo(pin, offset, divisor)
# grovepi.chainableRgbLed_setLevel(pin, level, reverse)

# test colors used in grovepi.chainableRgbLed_test()
testColorBlack = 0   # 0b000 #000000
testColorBlue = 1    # 0b001 #0000FF
testColorGreen = 2   # 0b010 #00FF00
testColorCyan = 3    # 0b011 #00FFFF
testColorRed = 4     # 0b100 #FF0000
testColorMagenta = 5 # 0b101 #FF00FF
testColorYellow = 6  # 0b110 #FFFF00
testColorWhite = 7   # 0b111 #FFFFFF

# patterns used in grovepi.chainableRgbLed_pattern()
thisLedOnly = 0
allLedsExceptThis = 1
thisLedAndInwards = 2
thisLedAndOutwards = 3

try:

    print("Test 1) Initialise")

    # init chain of leds
    grovepi.chainableRgbLed_init(pin, numleds)
    time.sleep(.5)

    # change color to green
    grovepi.storeColor(0,255,0)
    time.sleep(.5)

    # set led 1 to green
    grovepi.chainableRgbLed_pattern(pin, thisLedOnly, 0)
    time.sleep(.5)

    # change color to red
    grovepi.storeColor(255,0,0)
    time.sleep(.5)

    # set led 10 to red
    grovepi.chainableRgbLed_pattern(pin, thisLedOnly, 9)
    time.sleep(.5)

    # pause so you can see what happened
    time.sleep(2)

    # reset (all off)
    grovepi.chainableRgbLed_test(pin, numleds, testColorBlack)
    time.sleep(.5)


    print ("Test 2a) Test Patterns - black")

    # test pattern 0 - black (all off)
    grovepi.chainableRgbLed_test(pin, numleds, testColorBlack)
    time.sleep(1)


    print ("Test 2b) Test Patterns - blue")

    # test pattern 1 blue
    grovepi.chainableRgbLed_test(pin, numleds, testColorBlue)
    time.sleep(1)


    print ("Test 2c) Test Patterns - green")

    # test pattern 2 green
    grovepi.chainableRgbLed_test(pin, numleds, testColorGreen)
    time.sleep(1)


    print ("Test 2d) Test Patterns - cyan")

    # test pattern 3 cyan
    grovepi.chainableRgbLed_test(pin, numleds, testColorCyan)
    time.sleep(1)


    print ("Test 2e) Test Patterns - red")

    # test pattern 4 red
    grovepi.chainableRgbLed_test(pin, numleds, testColorRed)
    time.sleep(1)


    print ("Test 2f) Test Patterns - magenta")

    # test pattern 5 magenta
    grovepi.chainableRgbLed_test(pin, numleds, testColorMagenta)
    time.sleep(1)


    print ("Test 2g) Test Patterns - yellow")

    # test pattern 6 yellow
    grovepi.chainableRgbLed_test(pin, numleds, testColorYellow)
    time.sleep(1)


    print ("Test 2h) Test Patterns - white")

    # test pattern 7 white
    grovepi.chainableRgbLed_test(pin, numleds, testColorWhite)
    time.sleep(1)


    # pause so you can see what happened
    time.sleep(2)

    # reset (all off)
    grovepi.chainableRgbLed_test(pin, numleds, testColorBlack)
    time.sleep(.5)


    print ("Test 3a) Set using pattern - this led only")

    # change color to red
    grovepi.storeColor(255,0,0)
    time.sleep(.5)

    # set led 3 to red
    grovepi.chainableRgbLed_pattern(pin, thisLedOnly, 2)
    time.sleep(.5)

    # pause so you can see what happened
    time.sleep(2)

    # reset (all off)
    grovepi.chainableRgbLed_test(pin, numleds, testColorBlack)
    time.sleep(.5)


    print ("Test 3b) Set using pattern - all leds except this")

    # change color to blue
    grovepi.storeColor(0,0,255)
    time.sleep(.5)

    # set all leds except for 3 to blue
    grovepi.chainableRgbLed_pattern(pin, allLedsExceptThis, 3)
    time.sleep(.5)

    # pause so you can see what happened
    time.sleep(2)

    # reset (all off)
    grovepi.chainableRgbLed_test(pin, numleds, testColorBlack)
    time.sleep(.5)


    print ("Test 3c) Set using pattern - this led and inwards")

    # change color to green
    grovepi.storeColor(0,255,0)
    time.sleep(.5)

    # set leds 1-3 to green
    grovepi.chainableRgbLed_pattern(pin, thisLedAndInwards, 2)
    time.sleep(.5)

    # pause so you can see what happened
    time.sleep(2)

    # reset (all off)
    grovepi.chainableRgbLed_test(pin, numleds, testColorBlack)
    time.sleep(.5)


    print ("Test 3d) Set using pattern - this led and outwards")

    # change color to green
    grovepi.storeColor(0,255,0)
    time.sleep(.5)

    # set leds 7-10 to green
    grovepi.chainableRgbLed_pattern(pin, thisLedAndOutwards, 6)
    time.sleep(.5)

    # pause so you can see what happened
    time.sleep(2)

    # reset (all off)
    grovepi.chainableRgbLed_test(pin, numleds, testColorBlack)
    time.sleep(.5)


    print ("Test 4a) Set using modulo - all leds")

    # change color to black (fully off)
    grovepi.storeColor(0,0,0)
    time.sleep(.5)

    # set all leds black
    # offset 0 means start at first led
    # divisor 1 means every led
    grovepi.chainableRgbLed_modulo(pin, 0, 1)
    time.sleep(.5)

    # change color to white (fully on)
    grovepi.storeColor(255,255,255)
    time.sleep(.5)

    # set all leds white
    grovepi.chainableRgbLed_modulo(pin, 0, 1)
    time.sleep(.5)

    # pause so you can see what happened
    time.sleep(2)

    # reset (all off)
    grovepi.chainableRgbLed_test(pin, numleds, testColorBlack)
    time.sleep(.5)


    print ("Test 4b) Set using modulo - every 2")

    # change color to red
    grovepi.storeColor(255,0,0)
    time.sleep(.5)

    # set every 2nd led to red
    grovepi.chainableRgbLed_modulo(pin, 0, 2)
    time.sleep(.5)

    # pause so you can see what happened
    time.sleep(2)


    print ("Test 4c) Set using modulo - every 2, offset 1")

    # change color to green
    grovepi.storeColor(0,255,0)
    time.sleep(.5)

    # set every 2nd led to green, offset 1
    grovepi.chainableRgbLed_modulo(pin, 1, 2)
    time.sleep(.5)

    # pause so you can see what happened
    time.sleep(2)

    # reset (all off)
    grovepi.chainableRgbLed_test(pin, numleds, testColorBlack)
    time.sleep(.5)


    print ("Test 4d) Set using modulo - every 3, offset 0")

    # change color to red
    grovepi.storeColor(255,0,0)
    time.sleep(.5)

    # set every 3nd led to red
    grovepi.chainableRgbLed_modulo(pin, 0, 3)
    time.sleep(.5)

    # change color to green
    grovepi.storeColor(0,255,0)
    time.sleep(.5)

    # set every 3nd led to green, offset 1
    grovepi.chainableRgbLed_modulo(pin, 1, 3)
    time.sleep(.5)

    # change color to blue
    grovepi.storeColor(0,0,255)
    time.sleep(.5)

    # set every 3nd led to blue, offset 2
    grovepi.chainableRgbLed_modulo(pin, 2, 3)
    time.sleep(.5)

    # pause so you can see what happened
    time.sleep(2)

    # reset (all off)
    grovepi.chainableRgbLed_test(pin, numleds, testColorBlack)
    time.sleep(.5)


    print ("Test 4e) Set using modulo - every 3, offset 1")

    # change color to yellow
    grovepi.storeColor(255,255,0)
    time.sleep(.5)

    # set every 4nd led to yellow
    grovepi.chainableRgbLed_modulo(pin, 1, 3)
    time.sleep(.5)

    # pause so you can see what happened
    time.sleep(2)


    print ("Test 4f) Set using modulo - every 3, offset 2")

    # change color to magenta
    grovepi.storeColor(255,0,255)
    time.sleep(.5)

    # set every 4nd led to magenta
    grovepi.chainableRgbLed_modulo(pin, 2, 3)
    time.sleep(.5)

    # pause so you can see what happened
    time.sleep(2)

    # reset (all off)
    grovepi.chainableRgbLed_test(pin, numleds, testColorBlack)
    time.sleep(.5)


    print ("Test 5a) Set level 6")

    # change color to green
    grovepi.storeColor(0,255,0)
    time.sleep(.5)

    # set leds 1-6 to green
    grovepi.write_i2c_block(0x04,[95,pin,6,0])
    time.sleep(.5)

    # pause so you can see what happened
    time.sleep(2)

    # reset (all off)
    grovepi.chainableRgbLed_test(pin, numleds, testColorBlack)
    time.sleep(.5)


    print ("Test 5b) Set level 7 - reverse")

    # change color to red
    grovepi.storeColor(255,0,0)
    time.sleep(.5)

    # set leds 4-10 to red
    grovepi.write_i2c_block(0x04,[95,pin,7,1])
    time.sleep(.5)


except KeyboardInterrupt:
    # reset (all off)
    grovepi.chainableRgbLed_test(pin, numleds, testColorBlack)
except IOError:
    print ("Error")
