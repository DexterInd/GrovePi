# GrovePi + Grove Flame Sensor
# http://www.seeedstudio.com/wiki/Grove_-_Flame_Sensor

import time
import grovepi

# Connect the Grove Flame Sensor to digital port D2
# SIG,NC,VCC,GND
flame_sensor = 2

grovepi.pinMode(flame_sensor,"INPUT")

while True:
    try:
        print grovepi.digitalRead(flame_sensor)
        time.sleep(.5)

    except IOError:
        print "Error"
