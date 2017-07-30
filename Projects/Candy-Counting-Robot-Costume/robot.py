#!/usr/bin/env python
#
# Raspberry Pi Robot Costume
'''
In this project, we're making a Raspberry Pi Robot Costume.  The costume will count candy placed in a bin, and speak out loud to the giver.
Well use the GrovePi, with an Ultrasonic Sensor, an LED Bar graph, 4 Chainable LED's, and the RGB LCD Display.  We'll also use a small
portable speaker to give the robot a voice.  

Each time a piece of candy is placed in the robot, it says "Thank you for the candy" and reads aloud the count of candy.  
'''
#

import os
import random
import time
import grovepi
import sys
import random
from subprocess import call
from grove_rgb_lcd import *

candy_count = 10
bar_level = 0

led1 = 14
led2 = 15
led3 = 16

grovepi.pinMode(led1,"OUTPUT")
grovepi.pinMode(led2,"OUTPUT")
grovepi.pinMode(led3,"OUTPUT")

# Connect the Grove LED Bar to digital port D5
# DI,DCKI,VCC,GND
ledbar = 5

grovepi.pinMode(ledbar,"OUTPUT")
time.sleep(1)
i = 0

# Connect the Grove Ultrasonic Ranger to digital port D4
# SIG,NC,VCC,GND
ultrasonic_ranger = 4

# Connect first LED in Chainable RGB LED chain to digital port D7
# In: CI,DI,VCC,GND
# Out: CO,DO,VCC,GND
ledpin = 7	# RGB LED's are on D7
# First LED input socket connected to GrovePi, output socket connected to second LED input and so on
numleds = 4     #If you only plug 1 LED, change to 1
grovepi.pinMode(ledpin,"OUTPUT")
time.sleep(1)

# Connect the Grove 4 Digit Display to digital port D2
# CLK,DIO,VCC,GND
display = 2
grovepi.pinMode(display,"OUTPUT")

# test colors used in grovepi.chainableRgbLed_test()
testColorBlack = 0   # 0b000 #000000
testColorBlue = 1    # 0b001 #0000FF
testColorGreen = 2   # 0b010 #00FF00
testColorCyan = 3    # 0b011 #00FFFF
testColorRed = 4     # 0b100 #FF0000
testColorMagenta = 5 # 0b101 #FF00FF
testColorYellow = 6  # 0b110 #FFFF00
testColorWhite = 7   # 0b111 #FFFFFF

# patterns used in grovepi.chainableRgbLed_pattern()
thisLedOnly = 0
allLedsExceptThis = 1
thisLedAndInwards = 2
thisLedAndOutwards = 3

def initalize_chained_led():
		print("Test 1) Initialise")

		# init chain of leds
		grovepi.chainableRgbLed_init(ledpin, numleds)
		time.sleep(.5)

		grovepi.chainableRgbLed_test(ledpin, numleds, random.randint(0,7))
		time.sleep(.5)


def chained_led():
	try:

		# set led 1 to green
		grovepi.chainableRgbLed_pattern(pin, thisLedOnly, 0)
		time.sleep(.5)

		# change color to red
		grovepi.storeColor(255,0,0)
		time.sleep(.5)

		# reset (all off)
		grovepi.chainableRgbLed_test(pin, numleds, testColorBlack)
		time.sleep(.5)

		print ("Test 2b) Test Patterns - blue")

		# test pattern 1 blue
		grovepi.chainableRgbLed_test(pin, numleds, testColorBlue)
		time.sleep(1)

		print ("Test 2c) Test Patterns - green")

		# test pattern 2 green
		grovepi.chainableRgbLed_test(pin, numleds, testColorGreen)
		time.sleep(1)


		print ("Test 2d) Test Patterns - cyan")

		# test pattern 3 cyan
		grovepi.chainableRgbLed_test(pin, numleds, testColorCyan)
		time.sleep(1)


		print ("Test 2e) Test Patterns - red")

		# test pattern 4 red
		grovepi.chainableRgbLed_test(pin, numleds, testColorRed)
		time.sleep(1)


		print ("Test 2f) Test Patterns - magenta")

		# test pattern 5 magenta
		grovepi.chainableRgbLed_test(pin, numleds, testColorMagenta)
		time.sleep(1)


		print ("Test 2g) Test Patterns - yellow")

		# test pattern 6 yellow
		grovepi.chainableRgbLed_test(pin, numleds, testColorYellow)
		time.sleep(1)


		print ("Test 2h) Test Patterns - white")

		# test pattern 7 white
		grovepi.chainableRgbLed_test(pin, numleds, testColorWhite)
		time.sleep(1)


		# pause so you can see what happened
		time.sleep(2)

		# reset (all off)
		grovepi.chainableRgbLed_test(pin, numleds, testColorBlack)
		time.sleep(.5)


		print ("Test 3a) Set using pattern - this led only")

		# change color to red
		grovepi.storeColor(255,0,0)
		time.sleep(.5)

		# set led 3 to red
		grovepi.chainableRgbLed_pattern(pin, thisLedOnly, 2)
		time.sleep(.5)

		# pause so you can see what happened
		time.sleep(2)

		# reset (all off)
		grovepi.chainableRgbLed_test(pin, numleds, testColorBlack)
		time.sleep(.5)


		print ("Test 3b) Set using pattern - all leds except this")

		# change color to blue
		grovepi.storeColor(0,0,255)
		time.sleep(.5)

		# set all leds except for 3 to blue
		grovepi.chainableRgbLed_pattern(pin, allLedsExceptThis, 3)
		time.sleep(.5)

		# pause so you can see what happened
		time.sleep(2)

		# reset (all off)
		grovepi.chainableRgbLed_test(pin, numleds, testColorBlack)
		time.sleep(.5)


		print ("Test 3c) Set using pattern - this led and inwards")

		# change color to green
		grovepi.storeColor(0,255,0)
		time.sleep(.5)

		# set leds 1-3 to green
		grovepi.chainableRgbLed_pattern(pin, thisLedAndInwards, 2)
		time.sleep(.5)

		# pause so you can see what happened
		time.sleep(2)

		# reset (all off)
		grovepi.chainableRgbLed_test(pin, numleds, testColorBlack)
		time.sleep(.5)


		print ("Test 3d) Set using pattern - this led and outwards")

		# change color to green
		grovepi.storeColor(0,255,0)
		time.sleep(.5)

		# set leds 7-10 to green
		grovepi.chainableRgbLed_pattern(pin, thisLedAndOutwards, 6)
		time.sleep(.5)

		# pause so you can see what happened
		time.sleep(2)

		# reset (all off)
		grovepi.chainableRgbLed_test(pin, numleds, testColorBlack)
		time.sleep(.5)


		print ("Test 4a) Set using modulo - all leds")

		# change color to black (fully off)
		grovepi.storeColor(0,0,0)
		time.sleep(.5)

		# set all leds black
		# offset 0 means start at first led
		# divisor 1 means every led
		grovepi.chainableRgbLed_modulo(pin, 0, 1)
		time.sleep(.5)

		# change color to white (fully on)
		grovepi.storeColor(255,255,255)
		time.sleep(.5)

		# set all leds white
		grovepi.chainableRgbLed_modulo(pin, 0, 1)
		time.sleep(.5)

		# pause so you can see what happened
		time.sleep(2)

		# reset (all off)
		grovepi.chainableRgbLed_test(pin, numleds, testColorBlack)
		time.sleep(.5)


		print ("Test 4b) Set using modulo - every 2")

		# change color to red
		grovepi.storeColor(255,0,0)
		time.sleep(.5)

		# set every 2nd led to red
		grovepi.chainableRgbLed_modulo(pin, 0, 2)
		time.sleep(.5)

		# pause so you can see what happened
		time.sleep(2)


		print ("Test 4c) Set using modulo - every 2, offset 1")

		# change color to green
		grovepi.storeColor(0,255,0)
		time.sleep(.5)

		# set every 2nd led to green, offset 1
		grovepi.chainableRgbLed_modulo(pin, 1, 2)
		time.sleep(.5)

		# pause so you can see what happened
		time.sleep(2)

		# reset (all off)
		grovepi.chainableRgbLed_test(pin, numleds, testColorBlack)
		time.sleep(.5)


		print ("Test 4d) Set using modulo - every 3, offset 0")

		# change color to red
		grovepi.storeColor(255,0,0)
		time.sleep(.5)

		# set every 3nd led to red
		grovepi.chainableRgbLed_modulo(pin, 0, 3)
		time.sleep(.5)

		# change color to green
		grovepi.storeColor(0,255,0)
		time.sleep(.5)

		# set every 3nd led to green, offset 1
		grovepi.chainableRgbLed_modulo(pin, 1, 3)
		time.sleep(.5)

		# change color to blue
		grovepi.storeColor(0,0,255)
		time.sleep(.5)

		# set every 3nd led to blue, offset 2
		grovepi.chainableRgbLed_modulo(pin, 2, 3)
		time.sleep(.5)

		# pause so you can see what happened
		time.sleep(2)

		# reset (all off)
		grovepi.chainableRgbLed_test(pin, numleds, testColorBlack)
		time.sleep(.5)


		print ("Test 4e) Set using modulo - every 3, offset 1")

		# change color to yellow
		grovepi.storeColor(255,255,0)
		time.sleep(.5)

		# set every 4nd led to yellow
		grovepi.chainableRgbLed_modulo(pin, 1, 3)
		time.sleep(.5)

		# pause so you can see what happened
		time.sleep(2)


		print ("Test 4f) Set using modulo - every 3, offset 2")

		# change color to magenta
		grovepi.storeColor(255,0,255)
		time.sleep(.5)

		# set every 4nd led to magenta
		grovepi.chainableRgbLed_modulo(pin, 2, 3)
		time.sleep(.5)

		# pause so you can see what happened
		time.sleep(2)

		# reset (all off)
		grovepi.chainableRgbLed_test(pin, numleds, testColorBlack)
		time.sleep(.5)


		print ("Test 5a) Set level 6")

		# change color to green
		grovepi.storeColor(0,255,0)
		time.sleep(.5)

		# set leds 1-6 to green
		grovepi.write_i2c_block(0x04,[95,pin,6,0])
		time.sleep(.5)

		# pause so you can see what happened
		time.sleep(2)

		# reset (all off)
		grovepi.chainableRgbLed_test(pin, numleds, testColorBlack)
		time.sleep(.5)


		print ("Test 5b) Set level 7 - reverse")

		# change color to red
		grovepi.storeColor(255,0,0)
		time.sleep(.5)

		# set leds 4-10 to red
		grovepi.write_i2c_block(0x04,[95,pin,7,1])
		time.sleep(.5)


	except KeyboardInterrupt:
		# reset (all off)
		grovepi.chainableRgbLed_test(pin, numleds, testColorBlack)
	except IOError:
		print ("Error")


def led_random():
		#print "Change LED Color"
		# test pattern 1 blue
		try:
			grovepi.chainableRgbLed_test(ledpin, numleds, random.randint(0,7))
		# time.sleep(1)
		except:
			print "led_random failure"


def lcd_rgb(text):
	c = random.randint(0,255)
	setRGB(c,255-c,0)
	setText(text)

def lcd_rgb_blue_blank():
	setRGB(0,0,255)

#Calls the Espeak TTS Engine to read aloud a sentence
def sound(spk):
	#	-ven+m7:	Male voice
	#	-s180:		set reading to 180 Words per minute
	#	-k20:		Emphasis on Capital letters
	cmd_beg=" espeak -ven+m7 -a 200 -s180 -k20 --stdout '"
	cmd_end="' | aplay"
	print cmd_beg+spk+cmd_end
	call ([cmd_beg+spk+cmd_end], shell=True)


def LEDBarGraph(level):

	grovepi.ledBar_setLevel(ledbar,level)
	time.sleep(0.1)

def random_bar():
	global bar_level
	# print "Random bar! " + str(bar_level)
	try:
		ran_bar_sign = random.randint(0,1)
		if ran_bar_sign > 0:
			bar_level = bar_level + 1
		else:
			bar_level = bar_level - 1
		if bar_level < 0:
			bar_level = 0
		if bar_level > 10:
			bar_level = 10
		LEDBarGraph(bar_level)
	except:
		print "Random Bar Failure"

def random_led():
		try:
			grovepi.digitalWrite(led1,random.randint(0,1))
			grovepi.digitalWrite(led2,random.randint(0,1))
			grovepi.digitalWrite(led3,random.randint(0,1))
		except:
			print "LED Failure!"

def candy_detection():
	global candy_count
	dist = 100
	try:
		while dist > 8:
			# Read distance value from Ultrasonic
			# print(grovepi.ultrasonicRead(ultrasonic_ranger))
			dist = grovepi.ultrasonicRead(ultrasonic_ranger)
			random_bar()
			led_random()
		print("Distance Detected: " + str(dist))
		candy_count = candy_count + 1
		thanks = "Thank you for the candy! " + "I now have " + str(candy_count) + " pieces of candy!"
		lcd_rgb(str(thanks))
		led_random()
		sound(thanks)
	except TypeError:
		print ("Ultrasonic Error! Error!")
	except IOError:
		print ("Ultrasonic Error! Error!")

 

initalize_chained_led()	#Starts LED's sets to green.
grovepi.ledBar_init(ledbar, 0)
time.sleep(.5)

while True:
	led_random()
	random_bar()

	try:
		led_random()
		candy_detection()
	except:
		print "Error."
		lcd_rgb_blue_blank()
		random_bar()
		random_led()
		led_random()
	
	led_random()