#!/usr/bin/env python
#
# GrovePi Example for using the Grove - LCD RGB Backlight (http://www.seeedstudio.com/wiki/Grove_-_LCD_RGB_Backlight)
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://www.dexterindustries.com/forum/?forum=grovepi
#
# LICENSE: 
# These files have been made available online through a [Creative Commons Attribution-ShareAlike 3.0](http://creativecommons.org/licenses/by-sa/3.0/) license.

from grove_rgb_lcd import *

import random

try:
    setRGB(0,255,0)

    setText("Grove - LCD RGB Backlight")
    time.sleep(2)

    setText("Hello World")
    time.sleep(2)

    setText("Random colors")
    for i in range(0,51):
        setRGB(random.randint(0,255),random.randint(0,255),random.randint(0,255))
        time.sleep(.1)
    time.sleep(1)

    # ascii char 255 is the cursor character
    setRGB(255,255,255)
    setText(chr(255)*32)
    time.sleep(2)

    # typewriter
    setRGB(255,127,0)
    str = "Hello World"
    for i in range(0,12):
        setText(str[:i])
        time.sleep(.2)
    time.sleep(2)

    setRGB(255,0,255)
    setText("1234567890ABCDEF1234567890ABCDEF")
    time.sleep(2)

    setText("Long strings will be truncated at 32 chars")
    time.sleep(2)

    setRGB(0,255,0)
    setText("Automatic word wrapping")
    time.sleep(2)

    setText("Manual\nword wrapping")
    time.sleep(2)

    setRGB(0,255,255)
    setText("ASCII printable and extended")
    time.sleep(2)

    chars = ""
    for a in range(32,256):
        chars += chr(a)
        if len(chars) == 32:
            setText(chars)
            chars = ""
            time.sleep(2)

    setRGB(0,255,0)
    setText("Solid colors")
    time.sleep(2)

    setText("Red")
    setRGB(255,0,0)
    time.sleep(.5)

    setText("Green")
    setRGB(0,255,0)
    time.sleep(.5)

    setText("Blue")
    setRGB(0,0,255)
    time.sleep(.5)

    setText("Yellow")
    setRGB(255,255,0)
    time.sleep(.5)

    setText("Magenta")
    setRGB(255,0,255)
    time.sleep(.5)

    setText("Cyan")
    setRGB(0,255,255)
    time.sleep(.5)

    setText("White")
    setRGB(255,255,255)
    time.sleep(.5)

    setText("Black")
    setRGB(0,0,0)
    time.sleep(.5)

    setText("Grey")
    setRGB(127,127,127)
    time.sleep(.5)

    setRGB(255,255,255)
    setText("Alphanumeric characters")
    time.sleep(2)

    setText("1234567890ABCDEF1234567890ABCDEF")
    time.sleep(2)

    setText("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    time.sleep(2)

    setText("abcdefghijklmnopqrstuvwxyz")
    time.sleep(2)

    setText("1234567890")
    time.sleep(2)

    setText("Shades of red")
    for c in range(0,255):
        setRGB(255,255-c,255-c)
        time.sleep(.01)

    setText("Shades of green")
    for c in range(0,255):
        setRGB(255-c,255,255-c)
        time.sleep(.01)

    setText("Shades of blue")
    for c in range(0,255):
        setRGB(255-c,255-c,255)
        time.sleep(.01)

    setText("Shades of yellow")
    for c in range(0,255):
        setRGB(255,255,255-c)
        time.sleep(.01)

    setText("Shades of magenta")
    for c in range(0,255):
        setRGB(255,255-c,255)
        time.sleep(.01)

    setText("Shades of cyan")
    for c in range(0,255):
        setRGB(255-c,255,255)
        time.sleep(.01)

    setText("Shades of grey")
    for c in range(0,255):
        setRGB(c,c,c)
        time.sleep(.01)

except KeyboardInterrupt:
    setText("KeyboardInterrupt")
    setRGB(255,0,0)
except IOError:
    setText("IOError")
    setRGB(255,0,0)

time.sleep(1)
setText("All done")
setRGB(0,255,0)
