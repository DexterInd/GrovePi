# GrovePi + Grove Magnetic Switch
# http://www.seeedstudio.com/wiki/Grove_-_Magnetic_Switch

import time
import grovepi

# Connect the Grove Magnetic Switch to digital port D3
# SIG,NC,VCC,GND
magnetic_switch = 3

grovepi.pinMode(magnetic_switch,"INPUT")

while True:
    try:
        print grovepi.digitalRead(magnetic_switch)
        time.sleep(.5)

    except IOError:
        print "Error"
