# Tweet the temperature, light, and sound levels with our Raspberry Pi
# http://www.dexterindustries.com/GrovePi/projects-for-the-raspberry-pi/raspberry-pi-twitter-sensor-feed/

# GrovePi + Sound Sensor + Light Sensor + Temperature Sensor + LED
# http://www.seeedstudio.com/wiki/Grove_-_Sound_Sensor
# http://www.seeedstudio.com/wiki/Grove_-_Light_Sensor
# http://www.seeedstudio.com/wiki/Grove_-_Temperature_and_Humidity_Sensor_Pro
# http://www.seeedstudio.com/wiki/Grove_-_LED_Socket_Kit

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
'''

import twitter
import time
import grovepi
import math

# Connections
sound_sensor = 0        # port A0
light_sensor = 1        # port A1
temperature_sensor = 2  # port D2
led = 3                 # port D3

intro_str = "DI Lab's"

# Connect to Twitter
api = twitter.Api(
    consumer_key='YourKey',
    consumer_secret='YourKey',
    access_token_key='YourKey',
    access_token_secret='YourKey'
    )

grovepi.pinMode(led,"OUTPUT")
grovepi.analogWrite(led,255)  #turn led to max to show readiness


while True:


    # Error handling in case of problems communicating with the GrovePi
    try:

        # Get value from light sensor
        light_intensity = grovepi.analogRead(light_sensor)

        # Give PWM output to LED
        grovepi.analogWrite(led,light_intensity/4)

        # Get sound level
        sound_level = grovepi.analogRead(sound_sensor)

        time.sleep(0.5)

        # Get value from temperature sensor
        [t,h]=[0,0]
        [t,h] = grovepi.dht(temperature_sensor,0)

        # Post a tweet
        out_str ="%s Temp: %d C, Humidity: %d, Light: %d, Sound: %d" %(intro_str,t,h,light_intensity/10,sound_level)
        print (out_str)
        api.PostUpdate(out_str)
    except IOError:
        print("Error")
    except KeyboardInterrupt:
        exit()
    except Exception as e:
        print("Duplicate Tweet or Twitter Refusal: {}".format(e))

    time.sleep(60)
