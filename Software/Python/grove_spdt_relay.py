# GrovePi + Grove SPDT Relay(30A)
# http://www.seeedstudio.com/wiki/Grove_-_SPDT_Relay(30A)

import time
import grovepi

# Connect the Grove SPDT Relay to digital port D4
# SIG,NC,VCC,GND
relay = 4

# Relay is both normally open and normally closed.
# When the coil is energised, they will both flip.
# LED will illuminate when normally open is closed (and normally closed is open).

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
