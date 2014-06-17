# GrovePi + Grove Light Sensor
# http://www.seeedstudio.com/wiki/Grove_-_Light_Sensor

import time
import grovepi

# Connect the Light Sensor to analog port A0
light_sensor = 0

grovepi.pinMode(light_sensor,"INPUT")

while True:
    try:
        print grovepi.analogRead(light_sensor)
        time.sleep(.5)

    except IOError:
        print "Error"
