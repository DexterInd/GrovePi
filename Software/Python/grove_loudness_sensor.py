# GrovePi + Grove Loudness Sensor
# http://www.seeedstudio.com/wiki/Grove_-_Loudness_Sensor

import time
import grovepi

# Connect the Grove Loudness Sensor to analog port A0
# SIG,NC,VCC,GND
loudness_sensor = 0

while True:
    try:
        # Read the sound level
        sensor_value = grovepi.analogRead(loudness_sensor)

        print "sensor_value =", sensor_value
        time.sleep(.5)

    except IOError:
        print "Error"
