# GrovePi + Grove Electromagnet
# http://www.seeedstudio.com/wiki/Grove_-_Electromagnet

import time
import grovepi

# The electromagnet can hold a 1KG weight

# Connect the Grove Electromagnet to digital port D4
# SIG,NC,VCC,GND
electromagnet = 4

grovepi.pinMode(electromagnet,"OUTPUT")
time.sleep(1)

while True:
    try:
        # Switch on electromagnet
        grovepi.digitalWrite(electromagnet,1)
        print "on"
        time.sleep(2)

        # Switch off electromagnet
        grovepi.digitalWrite(electromagnet,0)
        print "off"
        time.sleep(2)

    except KeyboardInterrupt:
        grovepi.digitalWrite(electromagnet,0)
        break
    except IOError:
        print "Error"
