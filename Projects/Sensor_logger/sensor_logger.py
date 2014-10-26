# Temperature levels with our Raspberry Pi
# http://dexterindustries.com/GrovePi/projects-for-the-raspberry-pi/sensor-twitter-feed/

# GrovePi + Sound Sensor + Light Sensor + Temperature Sensor + LED
# http://www.seeedstudio.com/wiki/Grove_-_Temperature_and_Humidity_Sensor_Pro
# http://www.seeedstudio.com/wiki/Grove_-_LED_Socket_Kit

import time
import grovepi
import math
import datetime

# Connections 
temperature_sensor = 3  # port D3

#grovepi.pinMode(led,"OUTPUT")

def openFile():
	try:
		f = open("log.txt", "a")
		return f
	except IOError:
		print("File ERROR")
		openFile()

while True:
    # Error handling in case of problems communicating with the GrovePi
        # Get value from temperature sensor
        [temp,humidity] = grovepi.dht(temperature_sensor,0)
        t=temp
        h=humidity
        # Test
        #print ("Test Temp: %.2f, Hum: %d" %(t,h))
	
	now = datetime.datetime.now()	
	f = openFile()
	f.write(now.isoformat() + " || " +  "Temp: %.2f, Hum: %d \n" %(t,h))
	f.close()
        time.sleep(60)



