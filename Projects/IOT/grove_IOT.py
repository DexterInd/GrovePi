'''
## License
 GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
 Copyright (C) 2015  Dexter Industries

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/gpl-3.0.txt>.
'''

import xively
import datetime
import sys
import time
import grovepi

sensor = 4

XIVELY_API_KEY = "xmvAR7Y2KxAd00B8AFS1smKCsMigYheWFCybsx58sc2DmFOJ"
XIVELY_FEED_ID = "631205699"

api = xively.XivelyAPIClient(XIVELY_API_KEY)
feed = api.feeds.get(XIVELY_FEED_ID)

while True:
	try:
		now = datetime.datetime.utcnow()

		[temp,humidity] = grovepi.dht(sensor,1)
		light=int(grovepi.analogRead(0)/10.24)
		sound=int(grovepi.analogRead(1)/10.24)
		
		print temp,humidity,light,sound
		
		feed.datastreams = [
			xively.Datastream(id='temp', current_value=temp, at=now),
			xively.Datastream(id='humidity', current_value=humidity, at=now),
			xively.Datastream(id='light', current_value=light, at=now),
			xively.Datastream(id='sound', current_value=sound, at=now),
		]
		feed.update()
		time.sleep(10)
	except:
		print "Error"