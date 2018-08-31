#!/usr/bin/env python
#
# GrovePi Library for using the Grove - Temperature&Humidity Sensor (HDC1000)(http://www.seeedstudio.com/depot/Grove-TemperatureHumidity-Sensor-HDC1000-p-2535.html)
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this library?  Ask on the forums here:  http://forum.dexterindustries.com/c/grovepi
#
# This library is derived from the HDC1000 library by aklib here: https://github.com/nonNoise/akilib/blob/master/akilib/raspberrypi/AKI_I2C_HDC1000.py
#

# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information see https://github.com/DexterInd/GrovePi/blob/master/LICENSE

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

    def Config(self):
        # HDC1000 address, 0x40(64)
        # Select configuration register, 0x02(02)
        #		0x30(48)	Temperature, Humidity enabled, Resolultion = 14-bits, Heater on
        bus.write_byte_data(self.I2C_ADDR, 0x02, 0x30)

    def Temperature(self):
        try :
            bus.write_byte(self.I2C_ADDR,0x00)
            time.sleep(0.50)

            # Read data back, 2 bytes
            # temp MSB, temp LSB
            data0 = bus.read_byte(0x40)
            data1 = bus.read_byte(0x40)

            # Convert the data
            temp = (data0 * 256) + data1
            cTemp = (temp / 65536.0) * 165.0 - 40
            return cTemp
        except IOError as err:
            print("No ACK!")
            time.sleep(0.1)
            self.Temperature()

    def Humidity(self):
        try :
            bus.write_byte(self.I2C_ADDR,0x01)
            time.sleep(0.50)

            # Read data back, 2 bytes
            # humidity MSB, humidity LSB
            data0 = bus.read_byte(0x40)
            data1 = bus.read_byte(0x40)

            # Convert the data
            humidity = (data0 * 256) + data1
            humidity = (humidity / 65536.0) * 100.0
            return humidity
        except IOError as err:
            print("No ACK!")
            time.sleep(0.1)
            self.Humidity()
