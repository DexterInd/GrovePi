import smbus
import time
import grovepi
# for RPI version 1, use "bus = smbus.SMBus(0)"
bus = smbus.SMBus(0)

# This is the address we setup in the Arduino Program
address = 0x04

grovepi.pinMode(4,"OUTPUT")
time.sleep(1)
#similar to loop() of Arduino
while True:
	#digitalWrite() on pin 4 with HIGH
	grovepi.digitalWrite(4,1)
	time.sleep(1)
	#digitalWrite() on pin 4 with LOW
	grovepi.digitalWrite(4,0)
	time.sleep(1)
	
	