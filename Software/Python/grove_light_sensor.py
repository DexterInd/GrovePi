# GrovePi + Grove Light Sensor + LED
# http://www.seeedstudio.com/wiki/Grove_-_Light_Sensor
# http://www.seeedstudio.com/wiki/Grove_-_LED_Socket_Kit

import time
import grovepi

# Connect the Light Sensor to analog port A0
light_sensor = 0

# Connect the LED to digital port D4
led = 4

# Turn on LED once sensor exceeds threshold resistance
threshold = 10

grovepi.pinMode(light_sensor,"INPUT")
grovepi.pinMode(led,"OUTPUT")

while True:
    try:
        # Get sensor value
        v = grovepi.analogRead(light_sensor)

        # Calculate resistance of sensor in K
        R = (float)(1023 - v) * 10 / v;

        if R > threshold:
            # Send HIGH to switch on LED
            grovepi.digitalWrite(led,1)
        else:
            # Send LOW to switch off LED
            grovepi.digitalWrite(led,0)

        print v,R
        time.sleep(.5)

    except IOError:
        print "Error"
