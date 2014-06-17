# GrovePi + Grove Temperature Sensor
# http://www.seeedstudio.com/wiki/Grove_-_Temperature_Sensor

import grovepi

# Connect the Temperature Sensor to analog port A0
sensor = 0

while True:
    try:
        temp = grovepi.temp(sensor)
        print temp

    except IOError:
        print "Error"
