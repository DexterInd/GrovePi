#!/usr/bin/env python
#
# GrovePi Example for using the Grove Temperature & Humidity Sensor Pro 
# (http://www.seeedstudio.com/wiki/Grove_-_Temperature_and_Humidity_Sensor_Pro)
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  
# You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://forum.dexterindustries.com/c/grovepi
#
'''
## License

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
import json
from grovepi import *
from grove_rgb_lcd import *
from time import sleep
from math import isnan

with open('temp_hum.json','w') as my_json:


json.dump(temp_hum_details,my_json)

dht_sensor_port = 7 # connect the DHt sensor to port 7
dht_sensor_type = 0 # use 0 for the blue-colored sensor and 1 for the white-colored sensor

# set green as backlight color
# we need to do it just once
# setting the backlight color once reduces the amount of data transfer over the I2C line
setRGB(0,255,0)

while True:
try:
# get the temperature and Humidity from the DHT sensor
[ temp,hum ] = dht(dht_sensor_port,dht_sensor_type)

# change temp reading from celsius to fahrenheit
temp = ((temp/5.0)*9)+32

# round the temp to 2 decimal places so it will read on the LCD screen
new_temp = round(temp, 2)

print("temp =", temp , "F\thumidity =", hum,"%")

# check if we have nans
# if so, then raise a type error exception
if isnan(new_temp) is True or isnan(hum) is True:
raise TypeError('nan error')

t = str(new_temp)
h = str(hum)

# instead of inserting a bunch of whitespace, we can just insert a \n
# we're ensuring that if we get some strange strings on one line, the 2nd one won't be affected
setText_norefresh("Temp:" + t + "F\n" + "Humidity :" + h + "%")

except (IOError, TypeError) as e:
print(str(e))
# and since we got a type error
# then reset the LCD's text
setText("")
temp_hum_details= {

'temp' : temp,

'humidity' : hum

}

except KeyboardInterrupt as e:
print(str(e))
# since we're exiting the program
# it's better to leave the LCD with a blank text
setText("")
break
