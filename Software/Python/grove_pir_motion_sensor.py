#!/usr/bin/env python
#
# GrovePi Example for using the Grove PIR Motion Sensor (http://www.seeedstudio.com/wiki/Grove_-_PIR_Motion_Sensor)
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://www.dexterindustries.com/forum/?forum=grovepi
#
# LICENSE: 
# These files have been made available online through a [Creative Commons Attribution-ShareAlike 3.0](http://creativecommons.org/licenses/by-sa/3.0/) license.
#
# NOTE:
# 	There are also 2x potentiometers on the board for adjusting measuring distance and hold time
# 	Rotate the pot labelled "Delay time" clockwise to decrease the hold time (0.3s - 25s)
# 	Rotate the pot labelled "Distance" clockwise to decrease the measuring distance (10cm - 6m)
	
# 	There are multiple revisions of this board with different components for setting retriggerable/non-retriggerable.
# 	Revision 1.0 contains a switch and revision 1.2 contains a jumper hat.
# 	The 1.0 switch board is labelled with H,L - H=retriggerable, L=non-retriggerable.
# 	The 1.2 jumper board has a pin diagram printed on the back.
	
# 	retriggerable means the sensor will continue outputting high if motion was detected before the hold timer expires.
# 	non-retriggerable means the sensor will output high for the specified hold time only, then output low until motion is detected again.
# 	if there is constant motion detected, retriggerable will stay high for the duration and non-retriggerable will oscillate between high/low.

import time
import grovepi

# Connect the Grove PIR Motion Sensor to digital port D8
# SIG,NC,VCC,GND
pir_sensor = 8

grovepi.pinMode(pir_sensor,"INPUT")

while True:
    try:
        # Sense motion, usually human, within the target range
        if grovepi.digitalRead(pir_sensor):
            print 'Motion Detected'
        else:
            print '-'
        
        # if your hold time is less than this, you might not see as many detections
        time.sleep(.2)

    except IOError:
        print "Error"