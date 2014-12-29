# GrovePi + Grove Ultrasonic Ranger
# http://www.seeedstudio.com/wiki/Grove_-_Ultrasonic_Ranger

# This is an project using the Grove Ultrasonic Ranger and Relay from GrovePi start kit
# 
# In this project, the ultrasonic can figure out the distance of object in front, 
# when object close to it within 10cm, the relay will turn on

from grovepi import *

# Connect the Grove Ultrasonic Ranger to digital port D4
# SIG,NC,VCC,GND

ultrasonic_ranger = 4
Relay_pin = 2

pinMode(Relay_pin,"OUTPUT")

while True:
    try:
		# Read distance value from Ultrasonic
		distant = ultrasonicRead(ultrasonic_ranger)
		print distant,'cm'
		if distant <= 10:
			digitalWrite(Relay_pin,1)
		else:
			digitalWrite(Relay_pin,0)

    except TypeError:
        print "Error"
    except IOError:
        print "Error"
