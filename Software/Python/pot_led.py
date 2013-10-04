#Grove pi test with Pot and LED
import smbus
import time
import grovepi
# for RPI version 1, use "bus = smbus.SMBus(0)"
bus = smbus.SMBus(0)

# This is the address we setup in the Arduino Program
address = 0x04

grovepi.pinMode(5,"OUTPUT")
time.sleep(1)
i=0
while True:
	try:
		i=grovepi.analogRead(2)
		print i
		grovepi.analogWrite(3,i/4)
	except IOError:
		print "Error"
	
	
	
	