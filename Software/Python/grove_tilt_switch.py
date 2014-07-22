# GrovePi + Grove Tilt Switch
# http://www.seeedstudio.com/wiki/Grove_-_Tilt_Switch

import time
import grovepi

# Connect the Grove Tilt Switch to digital port D3
# SIG,NC,VCC,GND
tilt_switch = 3

grovepi.pinMode(tilt_switch,"INPUT")

while True:
    try:
        print grovepi.digitalRead(tilt_switch)
        time.sleep(.5)

    except IOError:
        print "Error"
