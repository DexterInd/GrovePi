#LED Fade Example
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
	if i>255:
		i=0
	grovepi.analogWrite(5,i)
	i=i+20
	time.sleep(.5)
	print grovepi.analogRead(0)
	time.sleep(1)
	
	
	