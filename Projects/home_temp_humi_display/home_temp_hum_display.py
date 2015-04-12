# home_temp_hum_display.py.py
#
# This is an project for using the Grove OLED Display and the Grove DHT Sensor from the GrovePi starter kit
# 
# In this project, the Temperature and humidity from the DHT sensor is printed on the DHT sensor

from grovepi import *
from grove_oled import *

dht_sensor_port = 7		# Connect the DHt sensor to port 7

#Start and initialize the OLED
oled_init()
oled_clearDisplay()
oled_setNormalDisplay()
oled_setVerticalMode()
time.sleep(.1)

while True:
	try:
		[ temp,hum ] = dht(dht_sensor_port,1)		#Get the temperature and Humidity from the DHT sensor
		print "temp =", temp, "C\thumidity =", hum,"%" 	
		t = str(temp)
		h = str(hum)
		
		oled_setTextXY(0,1)			#Print "WEATHER" at line 1
		oled_putString("WEATHER")
		
		oled_setTextXY(2,0)			#Print "TEMP" and the temperature in line 3
		oled_putString("Temp:")
		oled_putString(t+'C')
		
		oled_setTextXY(3,0)			#Print "HUM :" and the humidity in line 4
		oled_putString("Hum :")
		oled_putString(h+"%")
	except (IOError,TypeError) as e:
		print "Error"
