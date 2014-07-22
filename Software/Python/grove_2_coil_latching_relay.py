# GrovePi + Grove 2-Coil Latching Relay
# http://www.seeedstudio.com/wiki/Grove_-_2-Coil_Latching_Relay

import time
import grovepi

# Contrast to the ordinary relay, this latching relay does not need continuous power to keep the state, which makes it especially low power consumption

# Connect the Grove 2-Coil Latching Relay to digital port D4
# SIG,NC,VCC,GND
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
