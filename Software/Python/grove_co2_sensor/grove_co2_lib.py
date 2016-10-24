#!/usr/bin/env python
########################################################################               # GrovePi Library for using the Grove - CO2 Sensor(http://www.seeedstudio.com/depot/Grove-CO2-Sensor-p-1863.html)
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this library?  Ask on the forums here:  http://forum.dexterindustries.com/c/grovepi
#         
#
# NOTES:                                      
# * Calibration and read of the CO2 sensor MH-Z16 according to the datasheet : http://www.seeedstudio.com/wiki/images/c/ca/MH-Z16_CO2_datasheet_EN.pdf
# * output value directly in ppm
# * Library derived from the inital controbution by Doms Genoud (@domsgen) here: http://www.dexterindustries.com/topic/how-to-use-co2-grove-sensor-with-serial-grovepi/
# 
# History
# ------------------------------------------------
# Author     		Date      		Comments
# Doms Genoud      	13 Apr 15 		Initial Authoring
# Karan				07 Jan 16		Code cleanup and added to main Github repo
# 			                                                         
# These files have been made available online through a Creative Commons Attribution-ShareAlike 3.0  license.
# (http://creativecommons.org/licenses/by-sa/3.0/)           
#
########################################################################

import serial, time
import struct

ser = serial.Serial('/dev/ttyAMA0',  9600)	#Open the serial port at 9600 baud

class CO2:
#inspired from c code of http://www.seeedstudio.com/wiki/Grove_-_CO2_Sensor
#Gas concentration= high level *256+low level
	inp =[]
	cmd_zero_sensor = "\xff\x87\x87\x00\x00\x00\x00\x00\xf2"
	cmd_span_sensor = "\xff\x87\x87\x00\x00\x00\x00\x00\xf2"
	cmd_get_sensor = "\xff\x01\x86\x00\x00\x00\x00\x00\x79"
	
	def __init__(self):	
		#To open the raspberry serial port
		#ser = serial.Serial('/dev/ttyAMA0',  9600, timeout = 1)	#Open the serial port at 9600 baud

		#init serial
		ser.flush()
		
	def read(self):
		try:
			ser.write(self.cmd_get_sensor)
			self.inp = ser.read(9)
			high_level = struct.unpack('B',self.inp[2])[0]
			low_level = struct.unpack('B',self.inp[3])[0]
			temp_co2  =  struct.unpack('B',self.inp[4])[0] - 40

			#output in ppm, temp
			conc = high_level*256+low_level
			return [conc,temp_co2]

		except IOError:
			return [-1,-1]
			
if __name__ == "__main__":		
	c = CO2()
	while True:
		print(c.read())
		time.sleep(1)

