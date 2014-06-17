# GrovePi + Switch
# http://www.seeedstudio.com/wiki/Grove_-_Switch(P)

import time
import grovepi

# Connect the Switch to digital port D3
switch = 3

grovepi.pinMode(switch,"INPUT")

while True:
    try:
        print grovepi.digitalRead(switch)
        time.sleep(.5)

    except IOError:
        print "Error"
