#!/usr/bin/env python
# #######################################################################
# This library is for using the Grove Barometer module with he GrovePi
# http://www.dexterindustries.com/GrovePi/
# Barometer module: http://www.seeedstudio.com/depot/Grove-Barometer-HighAccuracy-p-1865.html
#
# History
# ------------------------------------------------
# Author    Date      		Comments
# Bill      26.07.2014   	Initial Port to Python
# Guruth    29.08.2014      Clean up and put to usable libary
#
# Re-written from: https://github.com/Seeed-Studio/Grove_Barometer_HP20x
# Refer to the datasheet to add additional functionality http://www.seeedstudio.com/wiki/images/d/d8/HP206C_Datasheet.pdf
########################################################################

# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information see https://github.com/DexterInd/GrovePi/blob/master/LICENSE


import smbus
import time
import RPi.GPIO as GPIO


rev = GPIO.RPI_REVISION
if rev == 2 or rev == 3:
    bus = smbus.SMBus(1)
else:
    bus = smbus.SMBus(0)

HP20X_I2C_DEV_ID = 0x76     # Barometer device address

HP20X_SOFT_RST = 0x06       # Soft reset the device
OK_HP20X_DEV = 0X80         # Default value for

HP20X_READ_PARA_REG = 0x8F  # Read Register

HP20X_ADC_CVT = 0x48        # Digital filter rate and channel

HP20X_READ_P = 0x30         # Read Pressure
HP20X_READ_A = 0x31         # Read Altitude
HP20X_READ_T = 0x32         # Read Temperature


class barometer:
    temperature = 0
    pressure = 0
    altitude = 0

    def __init__(self):
        # Send reset cmd to sensor
        bus.write_byte(HP20X_I2C_DEV_ID, HP20X_SOFT_RST)
        time.sleep(0.1)
        # Check if reset was successful
        if self.isAvailable():
            self.update()

    def isAvailable(self):
        # Read register status register
        bus.write_byte(HP20X_I2C_DEV_ID, HP20X_READ_PARA_REG)
        # Retrieve the value from he bus
        ret = bus.read_byte(HP20X_I2C_DEV_ID)
        # Check if reset was successful
        if ret == OK_HP20X_DEV:
            return True
        else:
            return False

    # Read sensor value
    def readSensor(self, sensor):
        # Set digital filter rate
        bus.write_byte(HP20X_I2C_DEV_ID, HP20X_ADC_CVT)
        time.sleep(.25)
        # Send cmd to read from sensor X
        # 0x30 || 0x31 || 0x32
        bus.write_byte(HP20X_I2C_DEV_ID, sensor)
        # Read data from bus
        data = bus.read_i2c_block_data(HP20X_I2C_DEV_ID, 0)
        value = data[0] << 16 | data[1] << 8 | data[2]
        return value

    # Update barometer values
    def update(self):
        # Read temp
        self.temperature = self.readSensor(HP20X_READ_T)
        time.sleep(0.2)
        # Read pressure
        self.pressure = self.readSensor(HP20X_READ_P)
        time.sleep(0.2)
        # Read altitude
        self.altitude = self.readSensor(HP20X_READ_A)
        time.sleep(0.2)
