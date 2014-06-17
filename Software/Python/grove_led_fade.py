# Fade LED in

# GrovePi + LED
# http://www.seeedstudio.com/wiki/Grove_-_LED_Socket_Kit

import time
import grovepi

# Connect the LED to digital port D5
led = 5

grovepi.pinMode(led,"OUTPUT")
time.sleep(1)
i = 0

while True:
    try:
        # Reset
        if i > 255:
            i = 0

        # Current brightness
        print i

        # Give PWM output to LED
        grovepi.analogWrite(led,i)

        # Increment brightness for next iteration
        i = i + 20
        time.sleep(.5)

    except KeyboardInterrupt:
        grovepi.analogWrite(led,0)
    except IOError:
        print "Error"