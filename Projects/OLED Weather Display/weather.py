#This is an example for the using the Grove OLED as a weather display
from grove_oled import *
import json
import urllib

#Get the weather
city="Chennai"
url="http://api.openweathermap.org/data/2.5/weather?q="+city
jsonurl = urllib.urlopen(url)
text = json.loads(jsonurl.read())

weather_desc=text["weather"][0]["description"]	# General description of the weather
temp=float(text["main"]["temp"])-273.15			# Temperature in C
pressure=text["main"]["pressure"]				# Pressure in hPa
humidity=text["main"]["humidity"]				# Humidity %
wind_speed=text["wind"]["speed"]				# Wind speed mps

print weather_desc,temp,pressure,humidity,wind_speed

#Print the data on the OLED

#Initialize the OLED
oled_init()
oled_clearDisplay()
oled_setNormalDisplay()
oled_setVerticalMode()
time.sleep(.1)

line=0
oled_setTextXY(line,0)
oled_putString("WEATHER:")
line+=2

oled_setTextXY(line,0)
oled_putString(weather_desc[:12])
line+=1

oled_setTextXY(line,0)
oled_putString("Temp:"+str(temp)+"C")
line+=1

oled_setTextXY(line,0)
oled_putString("Hum:"+str(humidity)+"%")
line+=1

oled_setTextXY(line,0)
oled_putString("Wind:"+str(wind_speed)+"mps")
line+=2

oled_setTextXY(line,0)
oled_putString("Pressure:")
line+=1

oled_setTextXY(line,0)
oled_putString(str(pressure)+"hPa")
