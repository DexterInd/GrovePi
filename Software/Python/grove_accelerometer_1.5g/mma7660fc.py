#
# History
# ------------------------------------------------
# Author	Date      		Comments
# Shoban	19 Sep 16	  	Initial Authoring
#
# Code derived from SwitchDoc Labs github repository: https://github.com/ControlEverythingCommunity/MMA7660FC
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
import time

# select the correct i2c bus for this revision of Raspberry Pi
revision = ([l[12:-1] for l in open('/proc/cpuinfo','r').readlines() if l[:8]=="Revision"]+['0000'])[0]
bus = smbus.SMBus(1 if int(revision, 16) >= 4 else 0)

# MMA7660FC constants
SENSITIVITY = 21.33 # Sensitivity = 21.33counts/g
EARTH_GRAVITY_MS2   = 9.80665    # 1g = 9.80665
ADDR        = 0x4c
MMA7660_X   = 0x00
MMA7660_Y   = 0x01
MMA7660_Z   = 0x02
TILT        = 0x03
SRST        = 0x04
SPCNT       = 0x05
INTSU       = 0x06
MODE        = 0x07
MODE_STAND_BY     = 0x00
MODE_ACTIVE       = 0x01
SR          = 0x08          #sample rate register
SR_AUTO_SLEEP_120 = 0X00    #120 sample per second
SR_AUTO_SLEEP_64  = 0X01
SR_AUTO_SLEEP_32  = 0X02
SR_AUTO_SLEEP_16  = 0X03
SR_AUTO_SLEEP_8   = 0X04
SR_AUTO_SLEEP_4   = 0X05
SR_AUTO_SLEEP_2   = 0X06
SR_AUTO_SLEEP_1   = 0X07
PDET       = 0x09
PD         = 0x0A

class MMA7660FC:
        def __init__(self):
                 self.address = ADDR
                 self.setMode(MODE_ACTIVE)
                 self.setSampleRate(SR_AUTO_SLEEP_1) #1 Sample/second active
        def setMode(self, Mode_Name):
                 bus.write_byte_data(self.address, MODE, Mode_Name)
	def setSampleRate(self, Sampling_Rate):
                 bus.write_byte_data(self.address, SR, Sampling_Rate)
                 time.sleep(0.5)
        def getAxes(self):
        # Read data back from 0x00, 3 bytes
                 data=bus.read_i2c_block_data(self.address, MMA7660_X, 3)
                 # Convert the data to 6-bits
                 xAccl = data[0] & 0x3F
                 if xAccl > 31 :
                        xAccl -= 64
                 # Convert the data to 6-bits
                 yAccl = data[1] & 0x3F
                 if yAccl > 31 :
                        yAccl -= 64
                 # Convert the data to 6-bits
                 zAccl = data[2] & 0x3F
                 if zAccl > 31 :
                        zAccl -= 64
	         
		 x = (xAccl * EARTH_GRAVITY_MS2)/SENSITIVITY
                 y = (yAccl * EARTH_GRAVITY_MS2)/SENSITIVITY
                 z = (zAccl * EARTH_GRAVITY_MS2)/SENSITIVITY

                 x = round(x, 4)
                 y = round(y, 4)
                 z = round(z, 4)
                 return{"x":x,"y":y,"z":y}
				 
if __name__ == "__main__":
    # if run directly we'll just create an instance of the class and output
    # the current readings
    mma7660fc = MMA7660FC()

    axes = mma7660fc.getAxes()
    print("MMA7660FC on address 0x%x:" % (mma7660fc.address))
    print("   x = %f m/s^2" % (axes['x']))
    print("   y = %f m/s^2" % (axes['y']))
    print("   z = %d m/s^2" % (axes['z']))


