# GrovePi + Grove Dry Reed Relay
# http://www.seeedstudio.com/wiki/Grove_-_Dry-Reed_Relay

import time
import grovepi

# Connect the Grove Dry Reed Relay to digital port D4
# SIG,NC,VCC,GND
relay = 4

# Relay is normally open. LED will illuminate when closed and there is no clicking sound

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
