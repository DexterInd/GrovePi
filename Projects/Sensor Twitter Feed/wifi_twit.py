# Temperature levels with our Raspberry Pi
# http://dexterindustries.com/GrovePi/projects-for-the-raspberry-pi/sensor-twitter-feed/

# GrovePi + Sound Sensor + Light Sensor + Temperature Sensor + LED
# http://www.seeedstudio.com/wiki/Grove_-_Temperature_and_Humidity_Sensor_Pro
# http://www.seeedstudio.com/wiki/Grove_-_LED_Socket_Kit

import time
import grovepi
import math

# Connections 
temperature_sensor = 0  # port A0

grovepi.pinMode(led,"OUTPUT")

last_sound = 0

while True:
    # Error handling in case of problems communicating with the GrovePi
    try:
        # Get value from temperature sensor
        [temp,humidity] = grovepi.dht(temperature_sensor,1)
        t=temp
        h=humidity
        # Test
        print ("Test Temp: %.2f, Hum: %d" %(t,h))
        time.sleep(3)
    except IOError:
        print ("error")
    except:
        print ("Duplicate Tweet")
