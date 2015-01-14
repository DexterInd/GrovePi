# GrovePi + Grove Relay
# http://www.seeedstudio.com/wiki/Grove_-_Relay

import time
import grovepi

# Connect the Grove Relay to digital port D4
# SIG,NC,VCC,GND
relay = 4

# Relay is normally open. LED will illuminate when closed and you will hear a definitive click sound

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
