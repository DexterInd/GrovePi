# wifi_finder.py
# Scan for open wifi networks!
# Uses - https://wifi.readthedocs.org/en/latest/wifi_command.html
# Install with pip install wifi
# Wifi dongle must be on wlan1 ; Check this with ifconfig.

from wifi import *
import time
import grovepi
from grove_rgb_lcd import *

## Connections
# LCD Goes on I2C-1
buzzer = 8		# Connect the Grove Buzzer to digital port D8
led = 4			# Connect the Grove LED to digital port D4

def check_open_ssids():
	open_ssids = []
	for cell in Cell.all('wlan1'):
		if cell.encrypted == False:
			# print cell.ssid
			open_ssids.append(cell.ssid)
	return open_ssids

def alert_user():
	# Buzz for 0.1 seconds
	grovepi.digitalWrite(buzzer,1)
	grovepi.digitalWrite(led,1)		# Send HIGH to switch on LED
	time.sleep(0.1)
	# Don't buzz for 0.1 seconds
	grovepi.digitalWrite(buzzer,0)
	grovepi.digitalWrite(led,0)		# Send LOW to switch off LED
	time.sleep(0.1)

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

		setRGB(0,255,0)
	except:
		print "Failed on something or other!"

	
while True:
	list_of_open = []
	# Test for any open ssids
	list_of_open = check_open_ssids()
	print list_of_open
	
	# If we find open ssids turn light and buzzer on, print to SSID.
	for ssid in list_of_open:
		display_ssid(ssid)
	
	# Look around ever 10 seconds.
	time.sleep(10)
	
