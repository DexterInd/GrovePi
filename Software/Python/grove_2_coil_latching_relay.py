#!/usr/bin/env python
#
# GrovePi Example for using a Grove 2-Coil Latching Relay(http://www.seeedstudio.com/wiki/Grove_-_2-Coil_Latching_Relay)
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://www.dexterindustries.com/forum/?forum=grovepi
#
# LICENSE: 
# These files have been made available online through a [Creative Commons Attribution-ShareAlike 3.0](http://creativecommons.org/licenses/by-sa/3.0/) license.
#
# NOTE: Contrast to the ordinary relay, this latching relay does not need continuous power to keep the state, which makes it especially low power consumption
import time
import grovepi

# Connect the Grove 2-Coil Latching Relay to digital port D4
# SIG,NC,VCC,GND
relay = 4

grovepi.pinMode(relay,"OUTPUT")

while True:
    try:
        # switch on for 5 seconds
        grovepi.digitalWrite(relay,1)
        print ("on")
        time.sleep(5)

        # switch off for 5 seconds
        grovepi.digitalWrite(relay,0)
        print ("off")
        time.sleep(5)

    except KeyboardInterrupt:
        grovepi.digitalWrite(relay,0)
        break
    except IOError:
        print ("Error")
