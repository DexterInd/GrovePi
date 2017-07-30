# GrovePi + Grove Ultrasonic Ranger
# http://www.seeedstudio.com/wiki/Grove_-_Ultrasonic_Ranger

# This is an project using the Grove Ultrasonic Ranger and Relay from GrovePi start kit
# 
# In this project, the ultrasonic can figure out the distance of object in front, 
# when object close to it within 10cm, the relay will turn on

'''
## License

The MIT License (MIT)

GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
Copyright (C) 2017  Dexter Industries

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
'''

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
        print(distant,'cm')
        if distant <= 10:
            digitalWrite(Relay_pin,1)
        else:
            digitalWrite(Relay_pin,0)

    except TypeError:
        print("Error")
    except IOError:
        print("Error")
