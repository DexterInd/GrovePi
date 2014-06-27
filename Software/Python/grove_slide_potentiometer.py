# GrovePi + Slide Potentiometer
# http://www.seeedstudio.com/wiki/Grove_-_Slide_Potentiometer

import time
import grovepi

# Connect the Slide Potentiometer to analog port A0
slide = 0   # pin 1 (yellow wire)

# The Slide Potentiometer has an onboard LED accessible as pin 2 on port A0
led = 1     # pin 2 (white wire)

grovepi.pinMode(slide,"INPUT")
grovepi.pinMode(led,"OUTPUT")
time.sleep(1)

while True:
    try:
        # Read sensor value from potentiometer
        sensor_value = grovepi.analogRead(slide)

        # Illuminate onboard LED
        if sensor_value > 500:
            grovepi.digitalWrite(led,1)
        else:
            grovepi.digitalWrite(led,0)

        print sensor_value

    except IOError:
        print "Error"
