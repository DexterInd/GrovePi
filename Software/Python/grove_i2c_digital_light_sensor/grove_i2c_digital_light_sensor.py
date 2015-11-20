#!/usr/bin/python

# Copyright 2014 IIJ Innovation Institute Inc. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY IIJ INNOVATION INSTITUTE INC. ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL IIJ INNOVATION INSTITUTE INC. OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Copyright 2014 Keiichi Shima. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE
# GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Code sourced from AdaFruit discussion board: https://www.adafruit.com/forums/viewtopic.php?f=8&t=34922
#
# Copyright 2014 Johan Vandewalle. All rights reserved.
#
# Redistributian and use in source and binary forms, with or without
# modification, are permitted provide that the following conditions are
# met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE
# GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

#import sensorbase
import time
import smbus
from Adafruit_I2C import Adafruit_I2C
import RPi.GPIO as GPIO
#import grovepi
from smbus import SMBus

global I2C_ADDRESS
global I2C_SMBUS
global _CMD
global _CMD_CLEAR
global _CMD_WORD
global _CMD_BLOCK
global _REG_CONTROL
global _REG_TIMING
global _REG_ID
global _REG_BLOCKREAD
global _REG_DATA0
global _REG_DATA1
global _POWER_UP
global _POWER_DOWN
global _GAIN_LOW
global _GAIN_HIGH
global _INTEGRATION_START
global _INTEGRATION_STOP
global _INTEGRATE_13
global _INTEGRATE_101
global _INTEGRATE_402
global _INTEGRATE_DEFAULT
global _INTEGRATE_NA
global _GAIN
global _MANUAL
global _INTEG
global _CHANNEL0
global _CHANNEL1
global _D0
global _D1
global _LUX


# bus parameters
rev = GPIO.RPI_REVISION
if rev == 2 or rev == 3:
    I2C_SMBUS = smbus.SMBus(1)
else:
    I2C_SMBUS = smbus.SMBus(0)

# Default I2C address
I2C_ADDRESS = 0x29

# Commands
_CMD       = 0x80
_CMD_CLEAR = 0x40
_CMD_WORD  = 0x20
_CMD_BLOCK = 0x10

# Registers
_REG_CONTROL   = 0x00
_REG_TIMING    = 0x01
_REG_ID        = 0x0A
_REG_BLOCKREAD = 0x0B
_REG_DATA0     = 0x0C
_REG_DATA1     = 0x0E

# Control parameters
_POWER_UP   = 0x03
_POWER_DOWN = 0x00

# Timing parameters
_GAIN_LOW          = 0b00000000
_GAIN_HIGH         = 0b00010000
_INTEGRATION_START = 0b00001000
_INTEGRATION_STOP  = 0b00000000
_INTEGRATE_13      = 0b00000000
_INTEGRATE_101     = 0b00000001
_INTEGRATE_402     = 0b00000010
_INTEGRATE_DEFAULT = _INTEGRATE_402
_INTEGRATE_NA      = 0b00000011

# Testing parameters
ambient  = None
IR       = None
_ambient = 0
_IR      = 0
_LUX     = None


class Tsl2561(object):
        i2c = None
        
        def _init__(self, bus = I2C_SMBUS, addr = I2C_ADDRESS, debug = 0, pause = 0.8):  # set debug = 0 stops debugging output on screen
                assert(bus is not None)
        	assert(addr > 0b000111 and addr < 0b1111000)

                self.i2c     = Adafruit_I2C(addr)
                self.pause   = pause
                self.debug   = debug
                self.gain    = 0
        	self._bus    = bus
                self._addr   = addr
                
        	ambient        = None
                IR             = None
        	self._ambient  = 0
                self._IR       = 0
        	self._LUX      = None
                self._control(_POWER_UP)
                self._partno_revision()
        
#        @property
        
        def _lux(self, gain):
                '''
                Returns a lux value.  Returns None if no valid value is set yet.
                '''
                var = readLux(gain)
                ambient = var[0]
                IR = var[1]
                self._ambient = var[2]
                self._IR = var[3]
                self_LUX = var[4]
                return (ambient, IR, self._ambient, self._IR, self._LUX)


        def setGain(self, gain = 1):
                """ Set the gain """
                if (gain != self.gain):
                        if (gain==1):
                                cmd = _CMD | _REG_TIMING
                                value = 0x02
                                self.i2c.write8(cmd, value)  # Set gain = 1X and timing = 402 mSec
                                if (self.debug):
                                        print "Setting low gain"
                        else:
                                cmd = _CMD | _REG_TIMING
                                value = 0x12
                                self.i2c.write8(cmd, value)  # Set gain = 16X and timing = 402 mSec
                                if (self.debug):
                                        print "Setting high gain"
                        self.gain=gain;  # Safe gain for calculation
                        time.sleep(self.pause)  # Pause for integration (self.pause must be bigger than integration time)

        
        def readWord(self, reg):
                """ Reads a word from the TSL2561 I2C device """
                try:
                        wordval = self.i2c.readU16(reg)
                        newval = self.i2c.reverseByteOrder(wordval)
                        if (self.debug):
                                print("I2C: Device 0x%02X: returned 0x%04X from reg 0x%02X" % (self._addr, wordval & 0xFFFF, reg))
                        return newval
                except IOError:
                        print("Error accessing 0x%02X: Chcekcyour I2C address" % self._addr)
                        return -1
                
        
        def readFull(self, reg = 0x8C):
                """ Read visible + IR diode from the TSL2561 I2C device """
                return self.readWord(reg);

        def readIR(self, reg = 0x8E):
                """ Reads only IR diode from the TSL2561 I2C device """
                return self.readWord(reg);
        
        def readLux(self, gain = 0):
                """ Grabs a lux reading either with autoranging (gain=0) or with specific gain (1, 16) """
                if (self.debug):
                        print "gain = ", gain
                if (gain == 1 or gain == 16):
                        self.setGain(gain)  # Low/highGain
                        ambient = self.readFull()
                        IR = self.readIR()
                elif (gain == 0):  # Auto gain
                        self.setGain(16)  # First try highGain
                        ambient = self.readFull()
                        if (ambient < 65535):
                                IR = self.readIR()
                        if (ambient >= 65535 or IR >= 65535):  # Value(s) exeed(s) datarange
                                self.setGain(1)  # Set lowGain
                                ambient = self.readFull()
                                IR = self.readIR()

                # If either sensor is saturated, no acculate lux value can be achieved.
                if (ambient == 0xffff or IR == 0xffff):
        		self._LUX = None
        		self._ambient = None
        		self._IR = None
        		return (self.ambient, self.IR, self._ambient, self._IR, self._LUX)
                if (self.gain == 1):
                        self._ambient = 16 * ambient  # Scale 1x to 16x
                        self._IR = 16 * IR            # Scale 1x to 16x
                else:
                        self._ambient = 1 * ambient
                        self._IR = 1 * IR
                if (self.debug):
                        print "IR Result without scaling: ", IR
                        print "IR Result: ", self._IR
                        print "Ambient Result without scaling: ", ambient
                        print "Ambient Result: ", self._ambient
                        
                if (self._ambient == 0):
         		# Sometimes, the channel 0 returns 0 when dark ...
        		self._LUX = 0.0
        		return (ambient, IR, self._ambient, self._IR, self._LUX)
        	
                ratio = (self._IR / float(self._ambient))  # Change to make it run under python 2

                if (self.debug):
                        print "ratio: ", ratio

                if ((ratio >= 0) and (ratio <= 0.52)):
                        self._LUX = (0.0315 * self._ambient) - (0.0593 * self._ambient * (ratio ** 1.4))
                elif (ratio <= 0.65):
                        self._LUX = (0.0229 * self._ambient) - (0.0291 * self._IR)
                elif (ratio <= 0.80):
                        self._LUX = (0.0157 * self._ambient) - (0.018 * self._IR)
                elif (ratio <= 1.3):
                        self._LUX = (0.00338 * self._ambient) - (0.0026 * self._IR)
                elif (ratio > 1.3):
                        self._LUX = 0

                return (ambient, IR, self._ambient, self._IR, self._LUX)
        
        def _partno_revision(self):
                """ Read Partnumber and revision of the sensor """
                cmd = _CMD | _REG_ID
                value = self.i2c.readS8(cmd)
                part = str(value)[7:4]
                if (part == "0000"):
                        PartNo = "TSL2560CS"
                elif (part == "0001"):
                        PartNo = "TSL2561CS"
                elif (part == "0100"):
                        PartNo = "TSL2560T/FN/CL"
                elif (part == "0101"):
                        PartNo = "TSL2561T/FN/CL"
                else:
                        PartNo = "not TSL2560 or TSL 2561"
                RevNo = str(value)[3:0]
                if (self.debug):
                        print "responce: ", value
                        print "PartNo = ", PartNo
                        print "RevNo = ", RevNo
                return (PartNo, RevNo)
        
        def _control(self, params):
                if (params == _POWER_UP):
                        print "Power ON"
                elif (params == _POWER_DOWN):
                        print "Power OFF"
                else:
                        print "No params given"
                cmd = _CMD | _REG_CONTROL | params
                self.i2c.write8(self._addr, cmd)  # select command register and power on
        	time.sleep(0.4)  # Wait for 400ms to power up or power down.
        
        

def main():
	TSL2561 = Tsl2561()
	TSL2561._init__(I2C_SMBUS, I2C_ADDRESS)
	while (True):
		gain=0
		val = TSL2561.readLux(gain)
		ambient = val[0]
		IR = val[1]
		_ambient = val[2]
		_IR = val[3]
		_LUX = val[4]
		if (ambient == 0xffff or IR == 0xffff):
			print ("\nSensor is saturated, no lux value can be achieved:")
			print ("ambient = " + ambient)
			print ("IR = " + IR)
			print ("light = " + _LUX)
		elif (_ambient == 0):
			print ("\nIt's dark:")
			print ("ambient = " + str(ambient))
			print ("IR = " + str(IR))
			print ("_ambient = " + str(_ambient))
			print ("_IR = " + str(_IR))
			print ("Light = " + str(_LUX) + " lux.")
		else:
			print ("\nThere is light:")
			print ("ambient = " + str(ambient))
			print ("IR = " + str(IR))
			print ("_ambient = " + str(_ambient))
			print ("_IR = " + str(_IR))
			print ("Light = " + str(_LUX) + " lux.")
		time.sleep(1)
		ambient  = None
		IR       = None
		_ambient = 0
		_IR      = 0
		_LUX     = None
		TSL2561._control(_POWER_DOWN)

        
if __name__=="__main__":
        main()
