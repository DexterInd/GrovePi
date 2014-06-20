# GrovePi + Switch + Relay
# http://www.seeedstudio.com/wiki/Grove_-_Switch(P)
# http://www.seeedstudio.com/wiki/Grove_-_Relay

import time
import grovepi

# Connect the Switch to digital port D3
switch = 3

# Connect the Relay to digital port D4
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
