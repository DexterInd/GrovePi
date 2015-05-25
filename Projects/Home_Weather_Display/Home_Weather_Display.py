# Home_Weather_Display.py
#
# This is an project for using the Grove RGB LCD Display and the Grove DHT Sensor from the GrovePi starter kit
# 
# In this project, the Temperature and humidity from the DHT sensor is printed on the RGB-LCD Display
#
#
# Note the second argument to the dht() call below - the type - may need to be changed depending on which DHT sensor you have:
#  0 - DHT11 – blue one - comes with the GrovePi+ Starter Kit
#  1 - DHT22 – white one, aka DHT Pro or AM2302
#  2 - DHT21 – black one, aka AM2301
#
# For more info please see: http://www.dexterindustries.com/forum/?topic=537-6c-displayed-in-home-weather-project/#post-4485
#
#

from grovepi import *
from grove_rgb_lcd import *

dht_sensor_port = 7		# Connect the DHt sensor to port 7

while True:
	try:
		[ temp,hum ] = dht(dht_sensor_port,1)		#Get the temperature and Humidity from the DHT sensor
		print "temp =", temp, "C\thumadity =", hum,"%" 	
		t = str(temp)
		h = str(hum)
		
		setRGB(0,128,64)
		setRGB(0,255,0)
		setText("Temp:" + t + "C      " + "Humidity :" + h + "%")			
	except (IOError,TypeError) as e:
		print "Error"
