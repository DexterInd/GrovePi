# rain_notifier.py
#
# This is an project that uses the Grove LED attached to an umbrella to remind people to take their umbrella if it's raining or going to rain

import urllib2
import json
from grovepi import *
import time

# Wunderground API Key
api_key='ADD_API_KEY_HERE'

# Zip code of location
zip='10001'
url='http://api.wunderground.com/api/'+api_key+'/geolookup/conditions/q/'+zip+'.json'

# Pin for the LED on the umbrella
led=7

pinMode(led,"OUTPUT")

while True:
	f = urllib2.urlopen(url)
	json_string = f.read()
	parsed_json = json.loads(json_string)
	location = parsed_json['location']['city']
	precip_today_in = parsed_json['current_observation']['precip_today_in']

	print "Current precipitation in %s is: %s" % (location, precip_today_in)

	if float(precip_today_in) > 0:
		print "Rains today, take the umbrella"
		# Light the LED on the umbrella
		digitalWrite(led,1)
	else:
		print "No Rains today"
		# Turn off the LED on the umbrella
		digitalWrite(led,0)
	f.close()
	time.sleep(60)