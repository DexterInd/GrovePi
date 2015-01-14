# GrovePi + Grove Temperature Sensor
# http://www.seeedstudio.com/wiki/Grove_-_Temperature_Sensor

import time
import grovepi

# Connect the Grove Temperature Sensor to analog port A0
# SIG,NC,VCC,GND
sensor = 0

# The sensor uses a thermistor to detect ambient temperature.
# The resistance of a thermistor will increase when the ambient temperature decreases.

# There are 3 revisions 1.0, 1.1 and 1.2, each using a different model thermistor.
# Each thermistor datasheet specifies a unique Nominal B-Constant which is used in the calculation forumla.

# The second argument in the grovepi.temp() method defines which board version you have connected.
# Defaults to '1.0'. eg.
# temp = grovepi.temp(sensor)        # B value = 3975
# temp = grovepi.temp(sensor,'1.1')  # B value = 4250
# temp = grovepi.temp(sensor,'1.2')  # B value = 4250

while True:
    try:
        temp = grovepi.temp(sensor,'1.1')
        print "temp =", temp
        time.sleep(.5)

    except KeyboardInterrupt:
        break
    except IOError:
        print "Error"
