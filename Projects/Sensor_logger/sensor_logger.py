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
temperature_sensor_in = 3  # port D3
temperature_sensor_out = 2 # port D2

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
            [temp,humidity] = grovepi.dht(temperature_sensor_in,0)
            t_in = temp
            h_in = humidity

            [temp,humidity] = grovepi.dht(temperature_sensor_out,1)
            t_out = temp
            h_out = humidity
            now = datetime.datetime.now()

            f = openFile()
            f.write(now.isoformat() + " || IN: " +  "Temp: %.2f, Hum: %d || OUT: Temp: %.2f, Hum: %d" %(t_in,h_in,t_out,h_out))
            f.close()

            time.sleep(60)

        except IOError:
            pass
        except:
            f = openFile()
            f.write("ERROR \n")
            f.close()
