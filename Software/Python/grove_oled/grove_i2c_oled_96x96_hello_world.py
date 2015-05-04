#!/usr/bin/env python
#
# GrovePi Example for using the Grove OLED Display 96*96 (http://www.seeedstudio.com/wiki/Grove_-_OLED_Display_1.12%22)
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://www.dexterindustries.com/forum/?forum=grovepi
#
# LICENSE: 
# These files have been made available online through a [Creative Commons Attribution-ShareAlike 3.0](http://creativecommons.org/licenses/by-sa/3.0/) license.

# Connect the OLED to any I2C port eg. I2C-1
# Can be found at I2C address 0x3c

import grove_oled
import time

grove_oled.oled_init()
grove_oled.oled_clearDisplay()
grove_oled.oled_setNormalDisplay()
grove_oled.oled_setVerticalMode()
time.sleep(.1)

for i in range(0,12):
    grove_oled.oled_setTextXY(i,0)
    grove_oled.oled_putString("Hello World")
