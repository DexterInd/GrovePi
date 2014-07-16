# GrovePi + Grove I2C 3-axis Accelerometer
# http://www.seeedstudio.com/wiki/Grove_-_3-Axis_Digital_Accelerometer(%C2%B11.5g)

import time
import grovepi

# Connect the Grove Accelerometer (+/- 1.5g) to any I2C port eg. I2C-1
# Can be found at I2C address 0x4c
# SCL,SDA,VCC,GND

while True:
    try:
        print grovepi.acc_xyz()
        time.sleep(.5)

    except IOError:
        print "Error"
