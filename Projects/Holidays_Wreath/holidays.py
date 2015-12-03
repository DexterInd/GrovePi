#!/usr/bin/env python
#
# GrovePi Example for using the Grove Relay (http://www.seeedstudio.com/wiki/Grove_-_Relay)
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://www.dexterindustries.com/forum/?forum=grovepi
#
'''
## License

The MIT License (MIT)

GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
Copyright (C) 2015  Dexter Industries

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
THE SOFTWARE.
'''
# NOTE: Relay is normally open. LED will illuminate when closed and you will hear a definitive click sound
import time
import grovepi

# Connect the Grove Relay to digital port D2
# SIG,NC,VCC,GND
relay = 2

# connect the PIR sensor to digital port D8
pir_sensor = 8

# connect the light sensor to analog port A0
light_sensor = 0

# how dark must it be before the lights turn on
light_threshold = 500

# delay when blinking lights. Currently on for 1 second, off for 1 second
blink_delay = 1

# initial status
lights_on = False


def blink(in_time):
    for i in range(in_time):
        grovepi.digitalWrite(relay,1)
        time.sleep(blink_delay)
        grovepi.digitalWrite(relay,0)
        time.sleep(blink_delay)
    if lights_on == True:
        grovepi.digitalWrite(relay,1)

grovepi.pinMode(relay,"OUTPUT")
grovepi.pinMode(pir_sensor,"INPUT")
grovepi.pinMode(light_sensor,"INPUT")


while True:
    try:
        blinky = grovepi.digitalRead(pir_sensor)
        if blinky:
            # switch on for 5 seconds
            print ("blink on")
            blink(5)
            print ("blink off")

        light_sensor_value = grovepi.analogRead(light_sensor)
        if light_sensor_value < light_threshold:
            # turn lights on
            if lights_on == False:
                lights_on = True
                print "turning lights on", light_sensor_value
                grovepi.digitalWrite(relay,1)
        
        else:
            # turn lights off
            if lights_on == True:
                lights_on = False
                print "turning lights off", light_sensor_value
                grovepi.digitalWrite(relay,0)
        

    except KeyboardInterrupt:
        grovepi.digitalWrite(relay,0)
        break
    except IOError as e:
        print ("I/O error({0}): {1}".format(e.errno, e.strerror))

    time.sleep(1)
