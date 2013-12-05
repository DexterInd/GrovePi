import twitter
import smbus
import time
import grovepi
import math
# for RPI version 1, use "bus = smbus.SMBus(0)"
bus = smbus.SMBus(0)

# This is the address of the Atmega328 on the GrovePi
address = 0x04

#Connect to twitter
api = twitter.Api(consumer_key='YourKey',consumer_secret='YourKey',access_token_key='YourKey',access_token_secret='YourKey')
print "Twitter Connected"
grovepi.pinMode(3,"OUTPUT")
last_sound=0
while True:
	#Error handling in case of problems communicating with the Grove Pi
	try:
		#Get value from temperature sensor
		t=grovepi.temp(2)
		#Get value from light sensor
		light_intensity=grovepi.analogRead(1)
		#Give PWM output to LED
		grovepi.analogWrite(3,light_intensity/4)
		#Get sound level
		sound_level=grovepi.analogRead(0)
		if sound_level>0:
			last_sound=sound_level
		#Post a tweet
		print ("DI Lab's Temp: %.2f, Light: %d, Sound: %d" %(t,light_intensity/10,last_sound))
		api.PostUpdate("DI Lab's Temp: %.2f, Light: %d, Sound: %d" %(t,light_intensity/10,last_sound))
		time.sleep(3)
	except IOError:
		print "Error"
	except:
		print "Duplicate Tweet"


	