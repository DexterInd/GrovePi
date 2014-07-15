# GrovePi + Grove Touch Sensor
# http://www.seeedstudio.com/wiki/Grove_-_Touch_Sensor

import time
import grovepi

# Connect the Grove Touch Sensor to digital port D4
# SIG,NC,VCC,GND
touch_sensor = 4

grovepi.pinMode(touch_sensor,"INPUT")

while True:
    try:
        print grovepi.digitalRead(touch_sensor)
        time.sleep(.5)

    except IOError:
        print "Error"
