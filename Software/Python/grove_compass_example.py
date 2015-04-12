#!/usr/bin/env python
#
# GrovePi Example for using the Grove Compass module (http://www.seeedstudio.com/depot/Grove-3Axis-Digital-Compass-p-759.html)
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://www.dexterindustries.com/forum/?forum=grovepi
#
# LICENSE: 
# These files have been made available online through a [Creative Commons Attribution-ShareAlike 3.0](http://creativecommons.org/licenses/by-sa/3.0/) license.

import grove_compass_lib
c=grove_compass_lib.compass()
while True:
	print "X:",c.x,"Y:",c.y,"X:",c.z,"Heading:",c.headingDegrees
	c.update()
	time.sleep(.1)