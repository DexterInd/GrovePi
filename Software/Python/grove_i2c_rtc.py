#!/usr/bin/env python
#
# GrovePi Example for using the Grove I2C RTC (http://www.seeedstudio.com/wiki/Grove_-_RTC)
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://www.dexterindustries.com/forum/?forum=grovepi
#
# LICENSE: 
# These files have been made available online through a [Creative Commons Attribution-ShareAlike 3.0](http://creativecommons.org/licenses/by-sa/3.0/) license.

import time
import grovepi

# Connect the Grove Real Time Clock to any I2C port eg. I2C-1
# Can be found at I2C address 0x68
# SCL,SDA,VCC,GND

while True:
    try:
        print (grovepi.rtc_getTime())
        time.sleep(.5)

    except IOError:
        print ("Error")
