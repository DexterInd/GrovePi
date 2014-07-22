# GrovePi + Grove Switch + Grove Relay
# http://www.seeedstudio.com/wiki/Grove_-_Switch(P)
# http://www.seeedstudio.com/wiki/Grove_-_Relay

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
