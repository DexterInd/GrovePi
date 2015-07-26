#This is an example for the using the Grove OLED as a weather display
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
