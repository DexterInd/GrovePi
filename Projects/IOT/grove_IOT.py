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