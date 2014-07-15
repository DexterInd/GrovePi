# GrovePi + Grove 80cm Infrared Proximity Sensor
# http://www.seeedstudio.com/wiki/Grove_-_80cm_Infrared_Proximity_Sensor

import time
import grovepi

# Connect the Grove 80cm Infrared Proximity Sensor to analog port A0
# SIG,NC,VCC,GND
sensor = 0

grovepi.pinMode(sensor,"INPUT")
time.sleep(1)

# Reference voltage of ADC is 5v
adc_ref = 5

# Vcc of the grove interface is normally 5v
grove_vcc = 5

while True:
    try:
        # Read sensor value
        sensor_value = grovepi.analogRead(sensor)

        # Calculate voltage
        voltage = round((float)(sensor_value) * adc_ref / 1024, 2)

        print "sensor_value =", sensor_value, " voltage =", voltage

    except IOError:
        print "Error"
