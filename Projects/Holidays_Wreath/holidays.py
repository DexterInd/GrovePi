#!/usr/bin/env python
#
# GrovePi Example for using the Grove Relay (http://www.seeedstudio.com/wiki/Grove_-_Relay)
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://forum.dexterindustries.com/c/grovepi
#
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
# you may want to adjust this if you have a street lamp or a porch light nearby
light_threshold = 500

# delay when blinking lights. Currently on for 1 second, off for 1 second
blink_delay = 1

# how long should the wreath be on after sunset (in hours)
hours_after_sunset = 5

# how long should the wreath sleep till sunrise (in hours)
hours_of_sleep = 6

# initial status
lights_on = False
start_sleeptime = time.time()

def sleeptime():
    """ 
    Calculates if it's time for the wreath to turn off for the night, and go to sleep 
    Contains a rather long sleep time (technically the whole night)
    """
    global lights_on
    now = time.time()
    go_to_sleep_time = start_sleeptime + (hours_after_sunset*60*60)
    # print now, start_sleeptime, "(", now-start_sleeptime,")", go_to_sleep_time, "(",go_to_sleep_time-now,")"
    if now >= go_to_sleep_time:
        print("Sleep time!!!")
        print("Will wake up in ", hours_of_sleep, " hours") 
        grovepi.digitalWrite(relay,0)
        lights_on = False
        for i in range(60):
            time.sleep(hours_of_sleep * 60  ) # long sleep time!!!
        print("Wake up!")

def blink(in_time):
    """
    blinks the wreath lights a certain number of times
    variable blink_delay determines how quick or slow the blink is
    in_time determines how many times the lights will blink
    """
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

##########################
# main loop
##########################
while True:
    try:
        # if the lights are on, test whether it's time for a long nappy
        if lights_on==True:
            sleeptime() # test included in this function call.

        if grovepi.digitalRead(pir_sensor):
            # switch on for 5 seconds
            print ("blink on")
            blink(5)
            print ("blink off")

        light_sensor_value = grovepi.analogRead(light_sensor)

        # is it getting dark?
        if light_sensor_value < light_threshold:
            # turn lights on
            if lights_on == False:
                lights_on = True
                start_sleeptime = time.time()
                print("turning lights on ") 
                grovepi.digitalWrite(relay,1)
        
        # is it getting light?
        else: 
            # turn lights off
            if lights_on == True:
                lights_on = False
                print("turning lights off", light_sensor_value)
                grovepi.digitalWrite(relay,0)
        

    except KeyboardInterrupt:
        grovepi.digitalWrite(relay,0)
        break
    except IOError as e:
        pass
    #    print ("I/O error({0}): {1}".format(e.errno, e.strerror))

    time.sleep(2)
