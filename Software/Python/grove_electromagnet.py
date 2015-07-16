#!/usr/bin/env python
#
# GrovePi Example for using the Grove Electromagnet (http://www.seeedstudio.com/wiki/Grove_-_Electromagnet)
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://www.dexterindustries.com/forum/?forum=grovepi
#
# LICENSE: 
# These files have been made available online through a [Creative Commons Attribution-ShareAlike 3.0](http://creativecommons.org/licenses/by-sa/3.0/) license.

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
