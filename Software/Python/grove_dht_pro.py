# GrovePi + Grove Temperature & Humidity Sensor Pro
# http://www.seeedstudio.com/wiki/Grove_-_Temperature_and_Humidity_Sensor_Pro

import grovepi

# Connect the Temperature & Humidity Sensor Pro to digital port D4
sensor = 4

while True:
    try:
        [temp,humidity] = grovepi.dht(sensor,1)
        print temp,humidity

    except IOError:
        print "Error"
