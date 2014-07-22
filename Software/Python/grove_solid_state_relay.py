# GrovePi + Grove Solid State Relay
# http://www.seeedstudio.com/wiki/Grove_-_Solid_State_Relay

import time
import grovepi

# Warnings:
# If the output voltage is higher than 36V, ensure the relay is in the off state before you operate with the terminal screws.
# The heatsink can get very hot during use.

# Connect the Grove Solid State Relay to digital port D4
# CTR,NC,VCC,GND
relay = 4

grovepi.pinMode(relay,"OUTPUT")

while True:
    try:
        # switch on for 5 seconds
        grovepi.digitalWrite(relay,1)
        print "on"
        time.sleep(5)

        # switch off for 5 seconds
        grovepi.digitalWrite(relay,0)
        print "off"
        time.sleep(5)

    except KeyboardInterrupt:
        grovepi.digitalWrite(relay,0)
        break
    except IOError:
        print "Error"
