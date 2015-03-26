#!/usr/bin/env python
#
# GrovePi Example for checking the firmware for the GrovePi
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://www.dexterindustries.com/forum/?forum=grovepi
#
# LICENSE: 
# These files have been made available online through a [Creative Commons Attribution-ShareAlike 3.0](http://creativecommons.org/licenses/by-sa/3.0/) license.
#
# NOTE: If you get a version of 255.255.255, they try running the script again, if the issue still persists then you are using an old deprecated firmware
import grovepi

try:
    print "GrovePi has firmware version:", grovepi.version()

except KeyboardInterrupt:
    print "KeyboardInterrupt"
except IOError:
    print "Error"
