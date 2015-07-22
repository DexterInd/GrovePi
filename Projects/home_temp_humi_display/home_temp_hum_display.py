# home_temp_hum_display.py.py
#
# This is an project for using the Grove OLED Display and the Grove DHT Sensor from the GrovePi starter kit
# 
# In this project, the Temperature and humidity from the DHT sensor is printed on the DHT sensor
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
