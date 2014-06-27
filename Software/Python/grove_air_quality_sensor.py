# GrovePi + Grove Air Quality Sensor
# http://www.seeedstudio.com/wiki/Grove_-_Air_Quality_Sensor

import time
import grovepi

# Wait 2 minutes for the sensor to heat-up

# Connect the Air Quality Sensor to analog port A0
air_sensor = 0

grovepi.pinMode(air_sensor,"INPUT")

while True:
    try:
        # Get sensor value
        v = grovepi.analogRead(air_sensor)

        if v > 700:
            print "High pollution"
        elif v > 300:
            print "Low pollution"
        else:
            print "Air fresh"

        print v
        time.sleep(.5)

    except IOError:
        print "Error"
