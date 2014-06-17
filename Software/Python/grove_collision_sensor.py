# GrovePi + Grove Collision Sensor
# http://www.seeedstudio.com/wiki/Grove_-_Collision_Sensor

import time
import grovepi

# Connect the Collision Sensor to digital port D2
collision_sensor = 2

grovepi.pinMode(collision_sensor,"INPUT")

while True:
    try:
        print grovepi.digitalRead(collision_sensor)
        time.sleep(.5)

    except IOError:
        print "Error"
