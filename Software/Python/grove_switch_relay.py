#!/usr/bin/env python
#
# GrovePi Example for using the Grove Switch and the Grove Relay
#
# Modules:
# 	http://www.seeedstudio.com/wiki/Grove_-_Switch(P)
# 	http://www.seeedstudio.com/wiki/Grove_-_Relay
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://www.dexterindustries.com/forum/?forum=grovepi
#
# LICENSE: 
# These files have been made available online through a [Creative Commons Attribution-ShareAlike 3.0](http://creativecommons.org/licenses/by-sa/3.0/) license.

import time
import grovepi

# Connect the Grove Switch to digital port D3
# SIG,NC,VCC,GND
switch = 3

# Connect the Grove Relay to digital port D4
# SIG,NC,VCC,GND
relay = 4

grovepi.pinMode(switch,"INPUT")
grovepi.pinMode(relay,"OUTPUT")

while True:
    try:
        if grovepi.digitalRead(switch):
            grovepi.digitalWrite(relay,1)
        else:
            grovepi.digitalWrite(relay,0)

        time.sleep(.5)

    except KeyboardInterrupt:
        grovepi.digitalWrite(relay,0)
        break
    except IOError:
        print "Error"
