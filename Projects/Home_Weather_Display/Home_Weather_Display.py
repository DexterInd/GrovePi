# grovepi_lcd_dht.py
#
# This is an project for using the Grove OLED Display and the Grove DHT Sensor from the GrovePi starter kit
# 
# In this project, the Temperature and humidity from the DHT sensor is printed on the DHT sensor

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
