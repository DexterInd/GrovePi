# GrovePi + Grove PH Sensor
# http://www.seeedstudio.com/wiki/Grove_-_PH_Sensor

import time
import grovepi

# Connect the Grove PH Sensor to analog port A0
# SIG,NC,VCC,GND
sensor = 0

grovepi.pinMode(sensor,"INPUT")
time.sleep(1)

# Reference voltage of ADC is 5v
adc_ref = 5

while True:
    try:
        # Read sensor value
        sensor_value = grovepi.analogRead(sensor)

        # Calculate PH
        ph = 7 - 1000 * (float)(sensor_value) * adc_ref / 59.16 / 1023

        print "sensor_value =", sensor_value, " ph =", ph

    except IOError:
        print "Error"
