# Tweet the temperature, light, and sound levels with our Raspberry Pi
# http://dexterindustries.com/GrovePi/projects-for-the-raspberry-pi/sensor-twitter-feed/

# GrovePi + Sound Sensor + Light Sensor + Temperature Sensor + LED
# http://www.seeedstudio.com/wiki/Grove_-_Sound_Sensor
# http://www.seeedstudio.com/wiki/Grove_-_Light_Sensor
# http://www.seeedstudio.com/wiki/Grove_-_Temperature_and_Humidity_Sensor_Pro
# http://www.seeedstudio.com/wiki/Grove_-_LED_Socket_Kit

import twitter
import time
import grovepi
import math

# Connections
sound_sensor = 0        # port A0
light_sensor = 1        # port A1 
temperature_sensor = 4  # port D4
led = 3                 # port D3

# Connect to Twitter
api = twitter.Api(consumer_key='YourKey',consumer_secret='YourKey',access_token_key='YourKey',access_token_secret='YourKey')
print "Twitter Connected"

grovepi.pinMode(led,"OUTPUT")

last_sound = 0

while True:
    # Error handling in case of problems communicating with the GrovePi
    try:
        # Get value from temperature sensor
        [temp,humidity] = grovepi.dht(temperature_sensor,1)
        t=temp

        # Get value from light sensor
        light_intensity = grovepi.analogRead(light_sensor)

        # Give PWM output to LED
        grovepi.analogWrite(led,light_intensity/4)

        # Get sound level
        sound_level = grovepi.analogRead(sound_sensor)
        if sound_level > 0:
            last_sound = sound_level

        # Post a tweet
        print ("DI Lab's Temp: %.2f, Light: %d, Sound: %d" %(t,light_intensity/10,last_sound))
        api.PostUpdate("DI Lab's Temp: %.2f, Light: %d, Sound: %d" %(t,light_intensity/10,last_sound))
        time.sleep(3)
    except IOError:
        print "Error"
    except:
        print "Duplicate Tweet"
