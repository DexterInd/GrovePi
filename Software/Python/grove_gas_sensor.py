# GrovePi + Grove Gas Sensor
# http://www.seeedstudio.com/wiki/Grove_-_Gas_Sensor
# http://www.seeedstudio.com/wiki/Grove_-_Gas_Sensor(MQ5)
# http://www.seeedstudio.com/wiki/Grove_-_Gas_Sensor(O%E2%82%82)

import time
import grovepi

# There are 5 gas sensors
# MQ2 - Combustible Gas, Smoke
# MQ3 - Alcohol Vapor
# MQ5 - LPG, Natural Gas, Town Gas
# MQ9 - Carbon Monoxide, Coal Gas, Liquefied Gas
# 02 - Oxygen

# The sensitivity can be adjusted by the onboard potentiometer

# Connect the Grove Gas Sensor to analog port A0
# SIG,NC,VCC,GND
gas_sensor = 0

grovepi.pinMode(gas_sensor,"INPUT")

while True:
    try:
        # Get sensor value
        sensor_value = grovepi.analogRead(gas_sensor)

        # Calculate gas density - large value means more dense gas
        density = (float)(sensor_value / 1024)

        print "sensor_value =", sensor_value, " density =", density
        time.sleep(.5)

    except IOError:
        print "Error"
