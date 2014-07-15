# GrovePi + Grove I2C RTC
# http://www.seeedstudio.com/wiki/Grove_-_RTC

import time
import grovepi

# Connect the Grove Real Time Clock to any I2C port eg. I2C-1
# Can be found at I2C address 0x68
# SCL,SDA,VCC,GND

while True:
    try:
        print grovepi.rtc_getTime()
        time.sleep(.5)

    except IOError:
        print "Error"
