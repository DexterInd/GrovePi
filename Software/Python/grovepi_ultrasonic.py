from grovepi import *
#similar to loop() of Arduino
pin=4
while True:
	print ultrasonicRead(pin)
	