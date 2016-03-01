#!/usr/bin/env python
#
# GrovePi Library for using the Grove - Temperature&Humidity Sensor (HDC1000)(http://www.seeedstudio.com/depot/Grove-TemperatureHumidity-Sensor-HDC1000-p-2535.html)
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this library?  Ask on the forums here:  http://www.dexterindustries.com/forum/?forum=grovepi
#
# This library is derived from the HDC1000 library by aklib here: https://github.com/nonNoise/akilib/blob/master/akilib/raspberrypi/AKI_I2C_HDC1000.py
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

import smbus 
import RPi.GPIO as GPIO
import time

rev = GPIO.RPI_REVISION
if rev == 2 or rev == 3:
    bus = smbus.SMBus(1)
else:
    bus = smbus.SMBus(0)
    
class HDC1000:
    I2C_ADDR = 0
    def __init__(self):
        self.I2C_ADDR=0x40
        
    def i2cReg(self,wr,addr=0x00,data=0x0000):
        try :
            if(wr == "w"):
                tmp = (data&0x00FF)<<8 | (data&0xFF00)>>8
                #print "W:0x%02X = 0x%04X" % (addr,data)
                return bus.write_word_data(self.I2C_ADDR,addr,tmp)
            elif(wr == "r"):
                tmp =  bus.read_word_data(self.I2C_ADDR,addr)
                tmp = (tmp&0x00FF)<<8 | (tmp&0xFF00)>>8               
                #print "R:0x%02X = 0x%04X" % (addr,tmp)
                return tmp
            else :
               return -1
        except IOError, err:
            print "No ACK!"
            time.sleep(0.1)
            self.i2cReg(wr,addr,data)
            
    def Config(self):
         # 0 - 7 bit = 0
         # 8bit :     HRES1 = 0
         # 9bit :     HRES2 = 0 14bit mode
         # 10bit :     TRES = 0
         # 11bit :     BTST = 0 (ReadOnly)
         # 12bit :     MODE = 0
         # 13bit :     Reserved = 0
         # 14bit :     Reserved = 0
         # 15bit :     RST = 0
         self.i2cReg('r',0xFE)
         self.i2cReg('r',0xFF)
         self.i2cReg('r',0x02)
         self.i2cReg('w',0x02,0x0000)
         self.i2cReg('r',0x02)
         time.sleep(0.01)
         
    def Temperature(self):
        try :
            bus.write_byte(self.I2C_ADDR,0x00)
            time.sleep(0.20)
            d=[0]*2
            # print self.i2c.read_block_data(I2C_ADDR,0x00)
            d[0] = bus.read_byte(self.I2C_ADDR) 
            time.sleep(0.001)
            d[1] = bus.read_byte(self.I2C_ADDR) 
            time.sleep(0.001)
            #print "0x%02X :0x%02X" % (d[0],d[1])
            raw = ( d[0]<<8 | d[1] )
            #print (float(raw)/(2**16))*(165-40)
            return float(raw)/65536.0*165.0-40.0
        except IOError, err:
            print "No ACK!"
            time.sleep(0.1)
            self.Temperature()

    def Humidity(self):
        try :
            bus.write_byte(self.I2C_ADDR,0x00)
            time.sleep(0.10)
            d=[0]*2
            d[0] = bus.read_byte(self.I2C_ADDR) 
            time.sleep(0.001)
            d[1] = bus.read_byte(self.I2C_ADDR) 
            time.sleep(0.001)
            #print "0x%02X :0x%02X" % (d[0],d[1])
            raw = ( d[0]<<8 | d[1] )
            return float(raw)/65536.0*100.0
        except IOError, err:
            print "No ACK!"
            time.sleep(0.1)
            self.Humidity()