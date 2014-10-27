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
        try:
            [temp,humidity] = grovepi.dht(temperature_sensor,0)
            t = temp
            h = humidity

            now = datetime.datetime.now()

            f = openFile()
            f.write(now.isoformat() + " || " +  "Temp: %.2f, Hum: %d \n" %(t,h))
            f.close()

            time.sleep(60)

        except IOError:
            pass
        except:
            f = openFile()
            f.write("ERROR \n")
            f.close()
