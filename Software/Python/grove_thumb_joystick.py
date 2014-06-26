# GrovePi + Grove Thumb Joystick
# http://www.seeedstudio.com/wiki/Grove_-_Thumb_Joystick

import time
import grovepi

# Connect the Thumb Joystick to analog port A0

# GrovePi Port A0 uses Arduino pins 0 and 1
# GrovePi Port A1 uses Arduino pins 1 and 2
# Don't plug anything into port A1 that uses pin 1
# Most Grove sensors only use 3 of their 4 pins, which is why the GrovePi shares Arduino pins between adjacent ports
# If the sensor has a pin definition SIG,NC,VCC,GND, the second (white) pin is not connected to anything

# Uses two pins - one for the X axis and one for the Y axis
grovepi.pinMode(0,"INPUT")
grovepi.pinMode(1,"INPUT")

# The Thumb Joystick is an analog device that outputs analog signal ranging from 0 to 1023
# The X and Y axes are two ~10k potentiometers and a momentary push button which shorts the x axis

# My joystick produces slightly different results to the specifications found on the url above
# I've listed both here:

# Specifications
#     Min  Typ  Max  Click
#  X  206  516  798  1023
#  Y  203  507  797

# My Joystick
#     Min  Typ  Max  Click
#  X  253  513  766  1020-1023
#  Y  250  505  769

while True:
    try:
        # Get X/Y coordinates
        x = grovepi.analogRead(0)
        y = grovepi.analogRead(1)

        # Calculate X/Y resistance
        Rx = (float)(1023 - x) * 10 / x
        Ry = (float)(1023 - y) * 10 / y

        # Was a click detected on the X axis?
        click = 1 if x >= 1020 else 0

        print x,y,Rx,Ry,click
        print ''
        time.sleep(.5)

    except IOError:
        print "Error"
