#!/usr/bin/env python
########################################################################                                                                  
# This example is for is the simplest GPS Script.  It reads the
# raw output of the GPS sensor on the GoPiGo or GrovePi and prints it.  
#
# GPS SENSOR GOES INTO RPISER PORT
#
#####################################################
#
# http://www.dexterindustries.com/GoPiGo/ 
# http://www.dexterindustries.com/GrovePi/                                                                
# History
# ------------------------------------------------
# Author     Date      		Comments
# John      2/25/2015		Initial Authoring
# John      6/17/2016		Add some comments.
# 			                                                         
# These files have been made available online through a Creative Commons Attribution-ShareAlike 3.0  license.
# (http://creativecommons.org/licenses/by-sa/3.0/)           
#
########################################################################

import serial, time
import smbus
import math
import RPi.GPIO as GPIO
import struct
import sys
import ir_receiver_check

if ir_receiver_check.check_ir():
	print("Disable IR receiver before continuing")
	exit()

ser = serial.Serial('/dev/ttyAMA0',  9600, timeout = 0)	#Open the serial port at 9600 baud
ser.flush()

def readlineCR():
    rv = ""
    while True:
        time.sleep(0.01)	# This is the critical part.  A small pause 
        					# works really well here.
        ch = ser.read()        
        rv += ch
        if ch=='\r' or ch=='':
            return rv

while True:
	#readlineCR()
	x=readlineCR()
	print(x)
	
########################################################################
#
#	The output should look like something below.
#
#
########################################################################
'''
$GPGGA,001929.799,,,,,0,0,,,M,,M,,*4C
$GPGSA,A,1,,,,,,,,,,,,,,,*1E
$GPGSV,1,1,00*79
$GPRMC,001929.799,V,,,,,0.00,0.00,060180,,,N*46
$GPGGA,001930.799,,,,,0,0,,,M,,M,,*44
$GPGSA,A,1,,,,,,,,,,,,,,,*1E
$GPGSV,1,1,00*79
$GPRMC,001930.799,V,,,,,0.00,0.00,060180,,,N*4E
$GPGGA,001931.799,,,,,0,0,,,M,,M,,*45
$GPGSA,A,1,,,,,,,,,,,,,,,*1E
$GPGSV,1,1,00*79
$GPRMC,001931.799,V,,,,,0.00,0.00,060180,,,N*4F
$GPGGA,001932.799,,,,,0,0,,,M,,M,,*46
$GPGSA,A,1,,,,,,,,,,,,,,,*1E
$GPGSV,1,1,00*79
$GPRMC,001932.799,V,,,,,0.00,0.00,060180,,,N*4C
$GPGGA,001933.799,,,,,0,0,,,M,,M,,*47
$GPGSA,A,1,,,,,,,,,,,,,,,*1E
$GPGSV,1,1,00*79
$GPRMC,001933.799,V,,,,,0.00,0.00,060180,,,N*4D
$GPGGA,001934.799,,,,,0,0,,,M,,M,,*40
$GPGSA,A,1,,,,,,,,,,,,,,,*1E
$GPGSV,1,1,00*79
$GPRMC,001934.799,V,,,,,0.00,0.00,060180,,,N*4A
$GPGGA,001935.799,,,,,0,0,,,M,,M,,*41
'''
