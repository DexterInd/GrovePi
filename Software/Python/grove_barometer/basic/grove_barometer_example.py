# This is an example for using the Grove Barometer module
# Compass module: http://www.seeedstudio.com/depot/Grove-Barometer-HighAccuracy-p-1865.html

from grove_barometer_lib import *
b = barometer()
while True():
	print "Temp:",b.temperature," Pressure:",b.pressure," Altitude:",b.altitude
	b.update()
	time.sleep(.1)
