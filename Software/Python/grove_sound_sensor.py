# GrovePi + Sound Sensor + LED
# http://www.seeedstudio.com/wiki/Grove_-_Sound_Sensor
# http://www.seeedstudio.com/wiki/Grove_-_LED_Socket_Kit

import time
import grovepi

# Connect the Sound Sensor to analog port A0
sound_sensor = 0

# Connect the LED to digital port D5
led = 5

grovepi.pinMode(sound_sensor,"INPUT")
grovepi.pinMode(led,"OUTPUT")

# The threshold to turn the led on 400.00 * 5 / 1024 = 1.95v
threshold_value = 400

while True:
    try:
        # Read the sound level
        sensor_value = grovepi.analogRead(sound_sensor)
        print sensor_value
        
        # If loud, illuminate LED, otherwise dim
        if sensor_value > threshold_value
            grovepi.digitalWrite(led,1)
        else:
            grovepi.digitalWrite(led,0)

        time.sleep(.5)

    except IOError:
        print "Error"
