# GrovePi + Grove PIR Motion Sensor
# http://www.seeedstudio.com/wiki/Grove_-_PIR_Motion_Sensor

import time
import grovepi

# Connect the PIR Motion Sensor to digital port D8
# There are also 2x potentiometers on the board for adjusting response speed and hold time
pir_sensor = 8

grovepi.pinMode(pir_sensor,"INPUT")

while True:
    try:
        # Sense motion, usually human, within the target range
        print grovepi.digitalRead(pir_sensor)
        time.sleep(.5)

    except IOError:
        print "Error"
