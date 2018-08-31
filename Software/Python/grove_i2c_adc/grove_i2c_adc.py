#!/usr/bin/env python
#
# GrovePi Library for using the Grove - I2C ADC(http://www.seeedstudio.com/depot/Grove-I2C-ADC-p-1580.html)
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this library?  Ask on the forums here:  http://forum.dexterindustries.com/c/grovepi
#

# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information see https://github.com/DexterInd/GrovePi/blob/master/LICENSE

import time,sys
import RPi.GPIO as GPIO
import smbus

# use the bus that matches your raspi version
rev = GPIO.RPI_REVISION
if rev == 2 or rev == 3:
    bus = smbus.SMBus(1)
else:
    bus = smbus.SMBus(0)

class ADC:
	address = None

	REG_ADDR_RESULT = 0x00
	REG_ADDR_ALERT  = 0x01
	REG_ADDR_CONFIG = 0x02
	REG_ADDR_LIMITL = 0x03
	REG_ADDR_LIMITH = 0x04
	REG_ADDR_HYST   = 0x05
	REG_ADDR_CONVL  = 0x06
	REG_ADDR_CONVH  = 0x07

	def __init__(self,address=0x55):
		self.address=address
		bus.write_byte_data(self.address, self.REG_ADDR_CONFIG,0x20)

	def adc_read(self):
		data=bus.read_i2c_block_data(self.address, self.REG_ADDR_RESULT, 2)
		raw_val=(data[0]&0x0f)<<8 | data[1]
		return raw_val

if __name__ == "__main__":
	adc= ADC()
	while True:
		print(adc.adc_read())
		time.sleep(.5)
