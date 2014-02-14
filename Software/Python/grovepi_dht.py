from grovepi import *
#similar to loop() of Arduino
while True:
	[temp,humidity]= dht(4,1)
	print temp,humidity
	