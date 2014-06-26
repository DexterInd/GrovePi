# GrovePi + Grove Electricity Sensor
# http://www.seeedstudio.com/wiki/Grove_-_Electricity_Sensor

import time
import grovepi

# Connect the Electricity Sensor to analog port A0
sensor = 0

grovepi.pinMode(sensor,"INPUT")

# Vcc of the grove interface is normally 5v
grove_vcc = 5

while True:
    try:
        # Get sensor value
        sensor_value = grovepi.analogRead(sensor)

        # Calculate amplitude current (mA)
        amplitude_current = (float)(sensor_value / 1024 * grove_vcc / 800 * 2000000)

        # Calculate effective value (mA)
        effective_value = amplitude_current / 1.414

        # minimum_current = 1 / 1024 * grove_vcc / 800 * 2000000 / 1.414 = 8.6(mA)
        # Only for sinusoidal alternating current

        print "The amplitude of the current is", amplitude_current, "mA"
        print "The effective value of the current is", effective_value, "mA"
        time.sleep(1)

    except IOError:
        print "Error"
