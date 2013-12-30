import smbus
import time
import grovepi
# for RPI version 1, use "bus = smbus.SMBus(0)"
bus = smbus.SMBus(0)

# This is the address we setup in the Arduino Program
address = 0x04

grovepi.pinMode(0,"INPUT")
time.sleep(1)
#similar to loop() of Arduino
while True:
	#digitalWrite() on pin 4 with HIGH 
	test_var = grovepi.analogRead(0)
	print test_var
	time.sleep(1)
	