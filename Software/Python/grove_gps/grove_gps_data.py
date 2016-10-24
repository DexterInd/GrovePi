#!/usr/bin/env python
#
# GrovePi Example for using the Grove GPS Module http://www.seeedstudio.com/depot/Grove-GPS-p-959.html?cPath=25_130
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://forum.dexterindustries.com/c/grovepi
#
'''
## License

The MIT License (MIT)

GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
Copyright (C) 2015  Dexter Industries

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
THE SOFTWARE.
'''
                                              
# History
# ------------------------------------------------
# Author     Date      		Comments
# Karan      21 Aug 14 		Initial Authoring
# Karan		 10 June 15		Updated the code to reflect the decimal GPS coordinates (contributed by rschmidt on the DI forums: http://www.dexterindustries.com/forum/?topic=gps-example-questions/#post-5668)
# Karan		 18 Mar 16		Updated code to handle conditions where no fix from satellite
#
#
#####################################################
#
# GPS SENSOR GOES INTO RPISER PORT
#
#####################################################
#
import serial, time
import smbus
import math
import RPi.GPIO as GPIO
import struct
import sys
import ir_receiver_check

enable_debug=1
enable_save_to_file=0

if ir_receiver_check.check_ir():
	print("Disable IR receiver before continuing")
	exit()
	
ser = serial.Serial('/dev/ttyAMA0',  9600, timeout = 0)	#Open the serial port at 9600 baud
ser.flush()

def cleanstr(in_str):
	out_str = "".join([c for c in in_str if c in "0123456789.-" ])
	if len(out_str)==0:
		out_str = "-1"
	return out_str

def safefloat(in_str):
	try:
		out_str = float(in_str)
	except ValueError:
		out_str = -1.0
	return out_str

class GPS:
	#The GPS module used is a Grove GPS module http://www.seeedstudio.com/depot/Grove-GPS-p-959.html
	inp=[]
	# Refer to SIM28 NMEA spec file http://www.seeedstudio.com/wiki/images/a/a0/SIM28_DATA_File.zip
	GGA=[]


	#Read data from the GPS
	def read(self):	
		while True:
			GPS.inp=ser.readline()
			if GPS.inp[:6] =='$GPGGA': # GGA data , packet 1, has all the data we need
				break
			time.sleep(0.1)     #without the cmd program will crash
		try:
			ind=GPS.inp.index('$GPGGA',5,len(GPS.inp))	#Sometimes multiple GPS data packets come into the stream. Take the data only after the last '$GPGGA' is seen
			GPS.inp=GPS.inp[ind:]
		except ValueError:
			print ("")
		GPS.GGA=GPS.inp.split(",")	#Split the stream into individual parts
		return [GPS.GGA]
		
	#Split the data into individual elements
	def vals(self):
		if enable_debug:
			print(GPS.GGA)
			
		time=GPS.GGA[1]
		
		if GPS.GGA[2]=='':  # latitude. Technically a float
			lat =-1.0
		else:
			lat=safefloat(cleanstr(GPS.GGA[2]))
		
		if GPS.GGA[3]=='':  # this should be either N or S
			lat_ns=""
		else:
			lat_ns=str(GPS.GGA[3])
			
		if  GPS.GGA[4]=='':  # longitude. Technically a float
			long=-1.0
		else:
			long=safefloat(cleanstr(GPS.GGA[4]))
		
		if  GPS.GGA[5]=='': # this should be either W or E
			long_ew=""
		else:
			long_ew=str(GPS.GGA[5])
			
		fix=int(cleanstr(GPS.GGA[6]))
		sats=int(cleanstr(GPS.GGA[7]))
		
		if  GPS.GGA[9]=='':
			alt=-1.0
		else:
			# change to str instead of float
			# 27"1 seems to be a valid value
			alt=str(GPS.GGA[9])
		return [time,fix,sats,alt,lat,lat_ns,long,long_ew]
	
	# Convert to decimal degrees
	def decimal_degrees(self, raw_degrees):
		try:
			degrees = float(raw_degrees) // 100
			d = float(raw_degrees) % 100 / 60
			return degrees + d
		except: 
			return raw_degrees


if __name__ == "__main__":
	g=GPS()
	if enable_save_to_file:
		f=open("gps_data.csv",'w')	#Open file to log the data
		f.write("name,latitude,longitude\n")	#Write the header to the top of the file
	ind=0
	while True:
		time.sleep(0.01)
		try:
			x=g.read()	#Read from GPS
			[t,fix,sats,alt,lat,lat_ns,longitude,long_ew]=g.vals()	#Get the individial values
				
			# Convert to decimal degrees
			if lat !=-1.0:
				lat = g.decimal_degrees(safefloat(lat))
				if lat_ns == "S":
					lat = -lat

			if longitude !=-1.0:
				longitude = g.decimal_degrees(safefloat(longitude))
				if long_ew == "W":
					longitude = -longitude
					
			# print ("Time:",t,"Fix status:",fix,"Sats in view:",sats,"Altitude",alt,"Lat:",lat,lat_ns,"Long:",long,long_ew)
			try:
				print("Time\t\t: %s\nFix status\t: %d\nSats in view\t: %d\nAltitude\t: %s\nLat\t\t: %f\nLong\t\t: %f") %(t,fix,sats,alt,lat,longitude)
			except:
				print("Time\t\t: %s\nFix status\t: %s\nSats in view\t: %s\nAltitude\t: %s\nLat\t\t: %s\nLong\t\t: %s") %(t,str(fix),str(sats),str(alt),str(lat),str(longitude))
				
			s=str(t)+","+str(safefloat(lat)/100)+","+str(safefloat(longitude)/100)+"\n"	
				
			if enable_save_to_file:
				f.write(s)	#Save to file
			time.sleep(2)
		except IndexError:
			print ("Unable to read")
		except KeyboardInterrupt:
			if enable_save_to_file:
				f.close()
			print ("Exiting")
			sys.exit(0)
		
