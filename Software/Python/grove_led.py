# GrovePi + LED
# http://www.seeedstudio.com/wiki/Grove_-_LED_Socket_Kit

import time
import grovepi

# Connect the LED to digital port D4
led = 4

grovepi.pinMode(led,"OUTPUT")
time.sleep(1)

while True:
    try:
        # Send HIGH to switch on LED
        grovepi.digitalWrite(led,1)
        time.sleep(1)

        # Send LOW to switch off LED
        grovepi.digitalWrite(led,0)
        time.sleep(1)

    except KeyboardInterrupt:
        grovepi.digitalWrite(led,0)
        break
    except IOError:
        print "Error"
