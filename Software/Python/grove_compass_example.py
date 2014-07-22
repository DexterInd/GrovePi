# This is an example for using the Grove Compass module
# Compass module: http://www.seeedstudio.com/depot/Grove-3Axis-Digital-Compass-p-759.html

from grove_compass_lib import *
c=compass()
while True:
	print "X:",c.x,"Y:",c.y,"X:",c.z,"Heading:",c.headingDegrees
	c.update()
	time.sleep(.1)