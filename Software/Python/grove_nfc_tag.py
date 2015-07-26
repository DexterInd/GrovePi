#!/usr/bin/env python
#
# GrovePi Example for using the Grove NFC Tag module (http://www.seeedstudio.com/wiki/Grove_%EF%BC%8D_NFC)
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://www.dexterindustries.com/forum/?forum=grovepi
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
# NOTE:
#	Only currently supports basic reading and writing bytes to the onboard EEPROM, 
#	no support for locking or anything clever, that stuff shouldn't be too hard to add if you
#	read the datasheet though

import time,sys
import RPi.GPIO as GPIO
import smbus

NFC_ADDR = 0x53

# use the bus that matches your raspi version
rev = GPIO.RPI_REVISION
if rev == 2 or rev == 3:
    bus = smbus.SMBus(1)
else:
    bus = smbus.SMBus(0)
    
# read data from the NFC tag EEPROM (length bytes)
def readNFCData(addr,length):
  bus.write_byte_data(NFC_ADDR,addr>>8,addr&0xff)
  result=[]
  for c in range(length):
    result.append(bus.read_byte(NFC_ADDR))
  return result

# write data to the NFC tag EEPROM  (writes <data> to byte address addr)
def writeNFCData(addr,data):
    for byte in data:
      bus.write_word_data(NFC_ADDR,addr>>8,(addr&0xff | (byte<<8)))
      time.sleep(0.01)
      addr+=1

# example code
if __name__=="__main__":         
    print (readNFCData(0,16)) # read some data from address 0
    time.sleep(0.1)
    writeNFCData(0,[11,12,13,14,15,16,17,18,19]) # write this data to address 0
    time.sleep(0.1)
    print( readNFCData(0,16)) # this should show the changed data

