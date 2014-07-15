# GrovePi + Grove Switch
# http://www.seeedstudio.com/wiki/Grove_-_Switch(P)

import time
import grovepi

# Connect the Grove Switch to digital port D3
# SIG,NC,VCC,GND
switch = 3

grovepi.pinMode(switch,"INPUT")

while True:
    try:
        print grovepi.digitalRead(switch)
        time.sleep(.5)

    except IOError:
        print "Error"
