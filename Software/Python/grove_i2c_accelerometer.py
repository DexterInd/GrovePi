#!/usr/bin/env python
#
# GrovePi Example for using the Grove I2C 3-axis Accelerometer (http://www.seeedstudio.com/wiki/Grove_-_3-Axis_Digital_Accelerometer(%C2%B11.5g))
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://www.dexterindustries.com/forum/?forum=grovepi
#
# LICENSE: 
# These files have been made available online through a [Creative Commons Attribution-ShareAlike 3.0](http://creativecommons.org/licenses/by-sa/3.0/) license.

import time
import grovepi

# Connect the Grove Accelerometer (+/- 1.5g) to any I2C port eg. I2C-1
# Can be found at I2C address 0x4c
# SCL,SDA,VCC,GND

while True:
    try:
        print (grovepi.acc_xyz())
        time.sleep(.5)

    except IOError:
        print ("Error")
