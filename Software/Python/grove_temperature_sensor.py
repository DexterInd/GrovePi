# GrovePi + Grove Temperature Sensor
# http://www.seeedstudio.com/wiki/Grove_-_Temperature_Sensor

import grovepi

# Connect the Grove Temperature Sensor to analog port A0
# SIG,NC,VCC,GND
sensor = 0

while True:
    try:
        temp = grovepi.temp(sensor)
        print "temp =", temp

    except IOError:
        print "Error"
