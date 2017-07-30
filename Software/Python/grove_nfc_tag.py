#!/usr/bin/env python
#
# GrovePi Example for using the Grove NFC Tag module (http://www.seeedstudio.com/wiki/Grove_%EF%BC%8D_NFC)
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://forum.dexterindustries.com/c/grovepi
#
'''
## License

The MIT License (MIT)

GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
Copyright (C) 2017  Dexter Industries

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
    print(readNFCData(0,16)) # read some data from address 0
    time.sleep(0.1)
    writeNFCData(0,[11,12,13,14,15,16,17,18,19]) # write this data to address 0
    time.sleep(0.1)
    print(readNFCData(0,16)) # this should show the changed data

