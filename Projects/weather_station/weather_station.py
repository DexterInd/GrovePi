#!/usr/bin/env python
#
# GrovePi Project for a Weather Station project.
#	*	Reads the data from pressure(BMP180), light, temperature and humidity sensor 
#		and takes pictures from the Pi camera periodically and logs them
#	*	Sensor Connections on the GrovePi:
#			-> Grove Pressure sensor (BMP 180)		- Any I2C port
#			-> Grove light sensor					- Port A2
#			-> Grove DHT sensors					- Port D4
#
# NOTE:
#	*	Make sure that the Pi camera is enabled and works. Directions here: https://www.raspberrypi.org/help/camera-module-setup/
#	
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://www.dexterindustries.com/forum/?forum=grovepi
#
'''
## License

The MIT License (MIT)

GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
Copyright (C) 2015  Dexter Industries

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

import time
import grovepi
import subprocess
import math
from grove_i2c_barometic_sensor_BMP180 import BMP085

#analog sensor port number
light_sensor			= 2

#digital sensor
temp_himidity_sensor	= 4

#temp_himidity_sensor type
#	grove starter kit comes with the bluew sensor
blue=0
white=1

#Initialize th3 pressure sensor
bmp = BMP085(0x77, 1)

#############
#test timings
time_for_sensor		= 2		#  4 seconds
time_for_picture	= 4	# 12 seconds

#	final
# time_for_sensor		= 1*60*60	#1hr
# time_for_picture		= 8*60*60	#8hr

time_to_sleep		= 1
log_file="weather_station_log.csv"

#Read the data from the sensors
def read_sensor():
	try:
		pressure=pressure = bmp.readPressure()/100.0
		light=grovepi.analogRead(light_sensor)
		[temp,humidity] = grovepi.dht(temp_himidity_sensor,white)
		#Return -1 in case of bad temp/humidity sensor reading
		if math.isnan(temp) or math.isnan(humidity):		#temp/humidity sensor sometimes gives nan
			return [-1,-1,-1,-1]
		return [pressure,light,temp,humidity]
	
	#Return -1 in case of sensor error
	except (IOError,TypeError) as e:
			return [-1,-1,-1,-1]

#Take a picture with the current time using the Raspberry Pi camera. Save it in the same folder
def take_picture():
	try:
		cmd="raspistill -t 1 -o plant_monitor_"+str(time.strftime("%Y_%m_%d__%H_%M_%S"))+".jpg"
		process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
		output = process.communicate()[0]
		print "Picture taken\n------------>\n"
	except:
		print "Camera problem,please check the camera connections and settings"

#Save the initial time, we will use this to find out when it is time to take a picture or save a reading
last_read_sensor=last_pic_time= int(time.time())

while True:
	curr_time_sec=int(time.time())
	
	# If it is time to take the sensor reading
	if curr_time_sec-last_read_sensor>time_for_sensor:
		[pressure,light,temp,humidity]=read_sensor()
		# If any reading is a bad reading, skip the loop and try again
		if pressure==-1 or light==-1:
			print "Bad reading"
			time.sleep(1)
			continue
		curr_time = time.strftime("%Y-%m-%d:%H-%M-%S")
		print ("Time:%s\npressure: %.2f hPa\nLight: %d\nTemp: %.2fC\nHumidity:%.2f %%\n" %(curr_time,pressure,light,temp,humidity))
		
		# Save the sensor reading to the CSV file
		f=open(log_file,'a')
		f.write("%s,%.2f,%d,%.2f,%.2f;\n" %(curr_time,pressure,light,temp,humidity))
		f.close()
		
		#Update the last read time
		last_read_sensor=curr_time_sec
	
	# If it is time to take the picture
	if curr_time_sec-last_pic_time>time_for_picture:
		take_picture()
		last_pic_time=curr_time_sec
	
	#Slow down the loop
	time.sleep(time_to_sleep)