# GrovePi + Grove Moisture Sensor
# http://www.seeedstudio.com/wiki/Grove_-_Moisture_sensor

import time
import grovepi

# Connect the Grove Moisture Sensor to analog port A0
# SIG,NC,VCC,GND
sensor = 0

# The wiki suggests the following sensor values:
# Min  Typ  Max  Condition
# 0    0    0    sensor in open air
# 0    20   300  sensor in dry soil
# 300  580  700  sensor in humid soil
# 700  940  950  sensor in water

# My sensor produced:
# Val  Condition
# 0    sensor in open air
# 18   sensor in dry soil
# 425  sensor in humid soil
# 690  sensor in water

while True:
    try:
        print grovepi.analogRead(sensor)
        time.sleep(.5)

    except KeyboardInterrupt:
        break
    except IOError:
        print "Error"
