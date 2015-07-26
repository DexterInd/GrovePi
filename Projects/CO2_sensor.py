#!/usr/bin/env python
########################################################################                                                                  
# Calibration and read of the CO2 sensor MH-Z16
# according to the datasheet : http://www.seeedstudio.com/wiki/images/c/ca/MH-Z16_CO2_datasheet_EN.pdf
# output value directly in ppm
# Doms made                                                              
# History
# ------------------------------------------------
# Author     Date      		Comments
# Doms      13 04 15 		Initial Authoring
# 			                                                         
'''
## License
 GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
 Copyright (C) 2015  Dexter Industries

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/gpl-3.0.txt>.
'''         
#
########################################################################
import os
import serial, time
import smbus
import math
import RPi.GPIO as GPIO
import struct
import sys
import datetime
import grovepi
import struct
from grovepi import *

#
__author__ = 'Doms Genoud'

#co2 sensor
#use an external usb to serial adapter
ser = serial.Serial('/dev/ttyUSB0',  9600, timeout = 1)	#Open the serial port at 9600 baud

#To open the raspberry serial port
#ser = serial.Serial('/dev/ttyAMA0',  9600, timeout = 1)	#Open the serial port at 9600 baud

#init serial
ser.flush()


############# carbon dioxid CO2 #####################
class CO2:
#inspired from c code of http://www.seeedstudio.com/wiki/Grove_-_CO2_Sensor
#Gas concentration= high level *256+low level
    inp =[]
    cmd_zero_sensor = "\xff\x87\x87\x00\x00\x00\x00\x00\xf2"
    cmd_span_sensor = "\xff\x87\x87\x00\x00\x00\x00\x00\xf2"
    cmd_get_sensor = "\xff\x01\x86\x00\x00\x00\x00\x00\x79"
    def read(self):
        try:
          while True:
                ser.write(CO2.cmd_get_sensor)
                CO2.inp = ser.read(9)
                high_level = struct.unpack('B',CO2.inp[2])[0]
                low_level = struct.unpack('B',CO2.inp[3])[0]
                temp_co2  =  struct.unpack('B',CO2.inp[4])[0] - 40

                #output in ppm
                conc = high_level*256+low_level
                return [conc,temp_co2]

        except IOError:
                return [-1,-1]

    def calibrateZero(self):
        try:
             ser.write(CO2.cmd_zero_sensor)
             print "CO2 sensor zero calibrated"

        except IOError:
                print "CO2 sensor calibration error"

    def calibrateSpan(self):
        try:
          while True:
                #ser.write(CO2.cmd_zero_sensor)
                print "CO2 sensor span calibrated"
                break

        except IOError:
                print "CO2 sensor calibration error"

########################################################################################################
#############   MAIN
########################################################################################################
# following the specs of the sensor :
# read the sensor, wait 3 minutes, set the zero, read the sensor
c = CO2()

while True:
    try:
        #CO2 sensor calib
        print "wait 3 minutes to warm up CO2 sensor"
        time.sleep(180)
        print "Read before calibration-->",c.read()

        print "calibrating..."
        co2 = c.calibrateZero()
        time.sleep(5)

        print "Read after calibration-->",c.read()

        print "DONE"
        break

    except IndexError:
        print "Unable to read"
    except KeyboardInterrupt:
        print "Exiting"
        sys.exit(0)
