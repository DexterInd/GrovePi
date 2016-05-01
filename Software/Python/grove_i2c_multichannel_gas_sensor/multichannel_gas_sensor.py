#!/usr/bin/env python
#NOTE:
# This sensor is on port 0x04, so not compatible with grovepi unless you load an alternate firmware
# This is work in progress, would need logic analyzer and arduino to get working
# Error:
#   Traceback (most recent call last):
#  File "multichannel_gas_sensor.py", line 67, in <module>
#    m= MutichannelGasSensor()
#  File "multichannel_gas_sensor.py", line 21, in __init__
#    if self.readR0() >= 0:
#  File "multichannel_gas_sensor.py", line 27, in readR0
#    rtnData = self.readData(0x11)
#  File "multichannel_gas_sensor.py", line 52, in readData
#    buffer=bus.read_i2c_block_data(self.address, cmd, 4)
#IOError: [Errno 5] Input/output error
#
# LINKS
# http://www.seeedstudio.com/wiki/Grove_-_Multichannel_Gas_Sensor
# https://github.com/Seeed-Studio/Mutichannel_Gas_Sensor
import time,sys
import RPi.GPIO as GPIO
import smbus

# use the bus that matches your raspi version
rev = GPIO.RPI_REVISION
if rev == 2 or rev == 3:
    bus = smbus.SMBus(1)
else:
    bus = smbus.SMBus(0)

class MutichannelGasSensor:
    address = None
    is_connected = 0
    res=[0]*3

    def __init__(self,address=0x04):
        self.address=address
        is_connected = 0
        if self.readR0() >= 0:
            self.is_connected = 1
    
    def readR0(self):
        rtnData = 0
        
        rtnData = self.readData(0x11)
        if(rtnData >= 0):
            self.res0[0] = rtnData
        else:
            return rtnData
            
        rtnData = self.readData(0x12)
        if(rtnData >= 0):
            self.res0[0] = rtnData
        else:
            return rtnData
            
        rtnData = self.readData(0x13)
        if(rtnData >= 0):
            self.res0[0] = rtnData
        else:
            return rtnData
        return 0    
        
    def readData(self,cmd):
        timeout = 0
        buffer=[0]*4
        checksum = 0
        rtnData = 0
        
        buffer=bus.read_i2c_block_data(self.address, cmd, 4)
        print(data)
        
        checksum = buffer[0] + buffer[1] + buffer[2]
        if checksum != buffer[3]:
            return -4
        rtnData = ((buffer[1] << 8) + buffer[2])
        
        return rtnData
   
    def sendI2C(self,cmd):
        bus.write_byte(self.address, cmd)


if __name__ == "__main__":		
	m= MutichannelGasSensor()