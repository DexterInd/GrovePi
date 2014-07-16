# GrovePi + Grove Infrared Distance Interrupt
# http://www.seeedstudio.com/wiki/Grove_-_IR_Distance_Interrupt

import time
import grovepi

# The sensitivity can be adjusted by the onboard potentiometer

# Calibration
# Hold the sensor facing an empty dark area
# Adjust the potentiometer until the onboard LED switches off
# When the LED switches off the sensor is calibrated
# If not, adjust the potentiometer again

# Connect the Grove Infrared Distance Interrupt Sensor to digital port D4
# SIG,NC,VCC,GND
sensor = 4

grovepi.pinMode(sensor,"INPUT")

while True:
    try:
        # Sensor returns LOW and onboard LED lights up when the
        # received infrared light intensity exceeds the calibrated level
        if grovepi.digitalRead(sensor) == 0:
            print "found something"
        else:
            print "nothing"

        time.sleep(.5)

    except IOError:
        print "Error"
