# GrovePi + Grove Line Finder
# http://www.seeedstudio.com/wiki/Twig_-_Line_Finder

import time
import grovepi

# Connect the Grove Line Finder to digital port D7
# SIG,NC,VCC,GND
line_finder = 7

grovepi.pinMode(line_finder,"INPUT")

while True:
    try:
        # Return HIGH when black line is detected, and LOW when white line is detected
        if grovepi.digitalRead(line_finder) == 1:
            print "black line detected"
        else:
            print "white line detected"

        time.sleep(.5)

    except IOError:
        print "Error"
