#This is an example for the using the Grove OLED as a weather display
'''
The MIT License (MIT)

GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
Copyright (C) 2017  Dexter Industries

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
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

print(weather_desc,temp,pressure,humidity,wind_speed)

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
