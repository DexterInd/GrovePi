# GrovePi + Grove Infrared Reflective Sensor
# http://www.seeedstudio.com/wiki/Grove_-_Infrared_Reflective_Sensor

import time
import grovepi

# The sensitivity can be adjusted by the onboard potentiometer

# Calibration
# Hold the sensor at the height you desire above a white surface
# Adjust the potentiometer until the onboard LED lights up
# Keep the same height and move above a black surface
# If the LED switches off the sensor is calibrated
# If not, adjust the potentiometer again

# Connect the Grove Infrared Reflective Sensor to digital port D4
# SIG,NC,VCC,GND
sensor = 4

grovepi.pinMode(sensor,"INPUT")

while True:
    try:
        # Sensor returns HIGH on a black surface and LOW on a white surface
        if grovepi.digitalRead(sensor) == 1:
            print "black surface detected"
        else:
            print "white surface detected"

        time.sleep(.5)

    except IOError:
        print "Error"
