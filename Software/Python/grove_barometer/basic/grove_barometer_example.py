#!/usr/bin/env python
#
# GrovePi Example for using the Grove Barometer module (http://www.seeedstudio.com/depot/Grove-Barometer-HighAccuracy-p-1865.html)
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://www.dexterindustries.com/forum/?forum=grovepi
#
# LICENSE: 
# These files have been made available online through a [Creative Commons Attribution-ShareAlike 3.0](http://creativecommons.org/licenses/by-sa/3.0/) license.

from grove_barometer_lib
b = grove_barometer_lib.barometer()
while True():
	print ("Temp:",b.temperature," Pressure:",b.pressure," Altitude:",b.altitude)
	b.update()
	time.sleep(.1)
