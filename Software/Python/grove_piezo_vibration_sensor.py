# GrovePi + Grove Piezo Vibration Sensor
# http://www.seeedstudio.com/wiki/Grove-_Piezo_Vibration_Sensor

import time
import grovepi

# The sensitivity can be adjusted by the onboard potentiometer

# Connect the Grove Piezo Vibration Sensor to analog port A0
# OUT,NC,VCC,GND
piezo = 0

grovepi.pinMode(piezo,"INPUT")

while True:
    try:
        # When vibration is detected, the sensor outputs a logic high signal
        print grovepi.analogRead(piezo)
        time.sleep(.5)

    except IOError:
        print "Error"
