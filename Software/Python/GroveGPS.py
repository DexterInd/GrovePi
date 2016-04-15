#
# GrovePi is an electronics board designed by Dexter Industries that you can connect to hundreds of 
# different sensors, so you can program them to monitor, control, and automate devices in your life.  
# See more about the GrovePi here:  http://www.dexterindustries.com/grovepi/
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

import serial, time
import smbus
import math
import RPi.GPIO as GPIO
import struct
import sys
 
ser = serial.Serial('/dev/ttyAMA0',  9600, timeout = 0)	#Open the serial port at 9600 baud
ser.flush()
 
def readlineCR():
    rv = ""
    while True:
        time.sleep(0.001)	# This is the critical part.  A small pause 
        					# works really well here.
        ch = ser.read()        
        rv += ch
        if ch=='\r' or ch=='':
            return rv
 
class GPS:
	#The GPS module used is a Grove GPS module http://www.seeedstudio.com/depot/Grove-GPS-p-959.html
	inp=[]
	# Refer to SIM28 NMEA spec file http://www.seeedstudio.com/wiki/images/a/a0/SIM28_DATA_File.zip
	GGA=[]
 
	#Read data from the GPS
	def read(self):	
		while True:
			# GPS.inp=ser.readline()
			GPS.inp = readlineCR()
			if GPS.inp[:6] =='$GPGGA': # GGA data , packet 1, has all the data we need
				break
			time.sleep(0.1)
		try:
			ind=GPS.inp.index('$GPGGA',5,len(GPS.inp))	#Sometimes multiple GPS data packets come into the stream. Take the data only after the last '$GPGGA' is seen
			GPS.inp=GPS.inp[ind:]
		except ValueError:
			print ""
		GPS.GGA=GPS.inp.split(",")	#Split the stream into individual parts
		return [GPS.GGA]
 
	#Split the data into individual elements
	def vals(self):
		time=GPS.GGA[1]
		lat=GPS.GGA[2]
		lat_ns=GPS.GGA[3]
		long=GPS.GGA[4]
		long_ew=GPS.GGA[5]
		fix=GPS.GGA[6]
		sats=GPS.GGA[7]
		alt=GPS.GGA[9]
		return [time,fix,sats,alt,lat,lat_ns,long,long_ew]
 
g=GPS()
f=open("gps_data.csv",'w')	#Open file to log the data
f.write("name,latitude,longitude\n")	#Write the header to the top of the file
ind=0
while True:
	try:
		x=g.read()	#Read from GPS
		[t,fix,sats,alt,lat,lat_ns,long,long_ew]=g.vals()	#Get the individial values
		print "Time:",t,"Fix status:",fix,"Sats in view:",sats,"Altitude",alt,"Lat:",lat,lat_ns,"Long:",long,long_ew
		s=str(t)+","+str(float(lat)/100)+","+str(float(long)/100)+"\n"	
		f.write(s)	#Save to file
		time.sleep(2)
	except IndexError:
		print "Unable to read"
	except KeyboardInterrupt:
		f.close()
		print "Exiting"
		sys.exit(0)
	except:
		print "Raw String appears to be empty."
