#!/usr/bin/env python
''' 
 wifi_finder.py
 Scan for open wifi networks!  This is a portable wifi hotspot finder.  See our project at www.dexterindustries.com/GrovePi for more information on turning this into a portable wifi hotspot finder.

 Software Setup Notes:
 	* This example uses https://wifi.readthedocs.org/en/latest/wifi_command.html.  Install with pip install wifi
 	* Wifi dongle must be on wlan0 ; Check this with the command "ifconfig" on the command line.
 Hardware Setup Notes:
 	* Buzzer goes on port 8 of the GrovePi.
 	* LED Goes on port 4 of the GrovePi.
 	* The LCD goes on I2C-1.  Check this with the command "sudo i2cdetect -y 1"

 The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi

 Have a question about this example?  Ask on the forums here:  http://forum.dexterindustries.com/c/grovepi
'''
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


from wifi import *
import time
import grovepi
from grove_rgb_lcd import *

## Connections
# LCD Goes on I2C-1
buzzer = 2		# Connect the Grove Buzzer to digital port D8
led = 3			# Connect the Grove LED to digital port D3

grovepi.pinMode(buzzer, "OUTPUT")
grovepi.pinMode(led, "OUTPUT")

def check_open_ssids():
	open_ssids = []
	for cell in Cell.all('wlan0'):
		if cell.encrypted == False:
			# print cell.ssid
			open_ssids.append(cell.ssid)
	return open_ssids

def alert_user():
	# Buzz for 0.1 seconds
	grovepi.digitalWrite(buzzer,1)
	grovepi.digitalWrite(led,1)		# Send HIGH to switch on LED
	time.sleep(0.5)
	# Don't buzz for 0.1 seconds
	grovepi.digitalWrite(buzzer,0)
	grovepi.digitalWrite(led,0)		# Send LOW to switch off LED
	time.sleep(0.5)

# Print the ssid name to the LCD, beep and turn the LED on and off.
def display_ssid(ssid):
	alert_user()
	string_out = "SSID Available: " + str(ssid)
	
	try:
		setText(string_out)
		setRGB(0,128,64)

		alert_user()

		for c in range(0,255):
			setRGB(c,255-c,0)
			time.sleep(0.01)

		time.sleep(3)
		setRGB(0,0,0)
	except:
		print("Failed on something or other!")


try:
	while True:

		list_of_open = []
		
		# 1). Test for any open ssids
		list_of_open = check_open_ssids()
		print(list_of_open)
		
		# 2). If we find open ssids turn light and buzzer on, print to SSID.
		for ssid in list_of_open:
			display_ssid(ssid)
		
		# 3). Look around ever 5 seconds.
		time.sleep(5)
except:
	pass
finally:
	setText("")
	setRGB(0,0,0)
	grovepi.digitalWrite(buzzer,0)
	grovepi.digitalWrite(led,0)

