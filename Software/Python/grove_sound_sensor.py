#!/usr/bin/env python
#
# GrovePi Example for using the Grove Sound Sensor and the Grove LED
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Modules:
#	 http://www.seeedstudio.com/wiki/Grove_-_Sound_Sensor
#	 http://www.seeedstudio.com/wiki/Grove_-_LED_Socket_Kit
#
# Have a question about this example?  Ask on the forums here:  http://www.dexterindustries.com/forum/?forum=grovepi
#
# LICENSE: 
# These files have been made available online through a [Creative Commons Attribution-ShareAlike 3.0](http://creativecommons.org/licenses/by-sa/3.0/) license.

import time
import grovepi

# Connect the Grove Sound Sensor to analog port A0
# SIG,NC,VCC,GND
sound_sensor = 0

# Connect the Grove LED to digital port D5
# SIG,NC,VCC,GND
led = 5

grovepi.pinMode(sound_sensor,"INPUT")
grovepi.pinMode(led,"OUTPUT")

# The threshold to turn the led on 400.00 * 5 / 1024 = 1.95v
threshold_value = 400

while True:
    try:
        # Read the sound level
        sensor_value = grovepi.analogRead(sound_sensor)

        # If loud, illuminate LED, otherwise dim
        if sensor_value > threshold_value:
            grovepi.digitalWrite(led,1)
        else:
            grovepi.digitalWrite(led,0)

        print ("sensor_value =", sensor_value)
        time.sleep(.5)

    except IOError:
        print ("Error")
