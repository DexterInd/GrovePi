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

def get_outside_weather(location = 'Bucharest,ro'):
	import pyowm # Do a 'sudo pip install pyowm' to get this module
	
	owm = pyowm.OWM()
	
	#forecast = owm.daily_forecast(location)
	
	observation = owm.weather_at_place(location)
	weather = observation.get_weather()

	return weather 
	

while True:
	try:
		[ temp,hum ] = dht(dht_sensor_port,1)		#Get the temperature and Humidity from the DHT sensor
		print "Temp =", temp, "C\tHumidity =", hum,"%" 	
		t = str(temp)
		h = str(hum)
		
		oled_setTextXY(0,1)			#Print "WEATHER" at line 1
		oled_putString("INSIDE")
		
		oled_setTextXY(2,0)			#Print "TEMP" and the temperature in line 3
		oled_putString("Temp:")
		oled_putString(t+'C')
		
		oled_setTextXY(3,0)			#Print "HUM :" and the humidity in line 4
		oled_putString("Hum :")
		oled_putString(h+"%")
		
		# This uses OpenWeatherMap via the PyOWM module; pywom module needs to be installed via pip, see https://github.com/csparpa/pyowm
		weather = get_outside_weather() # by default location is Bucharest,ro; change it to your own
		
		print "Weather: ", weather.get_temperature("celsius")
		print "Humidity: ", weather.get_humidity()

		oled_setTextXY(5,1)
		oled_putString("OUTSIDE")

		oled_setTextXY(7,0)
		oled_putString("Temp:")
		oled_putString(str(weather.get_temperature("celsius")['temp']) + "C")
		
		oled_setTextXY(8,0)
		oled_putString("Hum :")
		oled_putString(str(weather.get_humidity()) + "%")

		oled_setTextXY(9,0)
		oled_putString("Rain :")
		oled_putString(str(weather.get_rain()))

	except (IOError,TypeError,Exception) as e:
		print "Error"
