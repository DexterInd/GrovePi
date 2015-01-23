#Grove Analog Read sensor example
import time
import grovepi

#Sensor connected to A0 Port 
sensor = 1
grovepi.pinMode(sensor,"INPUT")
while True:
    try:
        sensor_value = grovepi.analogRead(sensor)

        print "sensor_value =", sensor_value
        time.sleep(.5)

    except IOError:
        print "Error"
