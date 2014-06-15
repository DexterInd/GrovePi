# GrovePi + Rotary Angle Sensor (Potentiometer) + LED
# http://www.seeedstudio.com/wiki/Grove_-_Rotary_Angle_Sensor
# http://www.seeedstudio.com/wiki/Grove_-_LED_Socket_Kit

import time
import grovepi

# Connect the Rotary Angle Sensor to analog port A2
potentiometer = 2

grovepi.pinMode(led,"OUTPUT")
time.sleep(1)
i = 0

while True:
    try:
        # Read resistance from Potentiometer
        print grovepi.analogRead(potentiometer)

    except IOError:
        print "Error"
