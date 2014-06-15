# GrovePi + Ultrasonic Ranger
# http://www.seeedstudio.com/wiki/Grove_-_Ultrasonic_Ranger

import grovepi

# Connect the Ultrasonic Ranger to digital port D4
ultrasonic_ranger = 4

while True:
    try:
        # Read distance value from Ultrasonic
        print ultrasonicRead(ultrasonic_ranger)

    except TypeError:
        print "Error"
    except IOError:
        print "Error"
