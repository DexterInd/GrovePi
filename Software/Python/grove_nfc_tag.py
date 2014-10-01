# GrovePi + Grove NFC Tag module
# http://www.seeedstudio.com/wiki/Grove_%EF%BC%8D_NFC
# Only currently supports basic reading and writing bytes to the onboard EEPROM, 
# no support for locking or anything clever, that stuff shouldn't be too hard to add if you
# read the datasheet though

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

