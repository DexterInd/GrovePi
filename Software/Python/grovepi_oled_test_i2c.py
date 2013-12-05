import smbus
import time
import grovepi
# for RPI version 1, use "bus = smbus.SMBus(0)"
bus = smbus.SMBus(0)

# This is the address we setup in the Arduino Program
address = 0x3c

def writeNumber(value):
    bus.write_byte(address, value)
    # bus.write_byte_data(address, 0, value) 
    return -1

def writeBlock(value):
	bus.write_i2c_block_data(address,0x80,value)
	return 1
	
def sendCommand(value):
	bus.write_i2c_block_data(address,0x80,[value])
	return 1
	
def sendData(value):
	bus.write_i2c_block_data(address,0x40,[value])
	return 1
	
def readNumber():
    number = bus.read_byte(address)
    # number = bus.read_byte_data(address, 1)
    return number

#grovepi.pinModae(7,"INPUT")
writeBlock([0x80])

sendCommand(0xFD)# // Unlock OLED driver IC MCU interface from entering command. i.e: Accept commands
sendCommand(0x12)#
sendCommand(0xAE)# // Set display off
sendCommand(0xA8)# // set multiplex ratio
sendCommand(0x5F)# // 96
sendCommand(0xA1)# // set display start line
sendCommand(0x00)#
sendCommand(0xA2)# // set display offset
sendCommand(0x60)#
sendCommand(0xA0)# // set remap
sendCommand(0x46)#
sendCommand(0xAB)# // set vdd internal
sendCommand(0x01)# //
sendCommand(0x81)# // set contrasr
sendCommand(0x53)# // 100 nit
sendCommand(0xB1)# // Set Phase Length
sendCommand(0X51)# //
sendCommand(0xB3)# // Set Display Clock Divide Ratio/Oscillator Frequency
sendCommand(0x01)#
sendCommand(0xB9)# //
sendCommand(0xBC)# // set pre_charge voltage/VCOMH
sendCommand(0x08)# // (0x08)#
sendCommand(0xBE)# // set VCOMH
sendCommand(0X07)# // (0x07)#
sendCommand(0xB6)# // Set second pre-charge period
sendCommand(0x01)# //
sendCommand(0xD5)# // enable second precharge and enternal vsl
sendCommand(0X62)# // (0x62)#
sendCommand(0xA4)# // Set Normal Display Mode
sendCommand(0x2E)# // Deactivate Scroll
sendCommand(0xAF)# // Switch on display
time.sleep(.1)

sendCommand(0x75)#; 	  // Set Row Address 
sendCommand(0x00)#; 	  // Start 0
sendCommand(0x5f)#; 	  // End 95 

sendCommand(0x15)#; 	  // Set Column Address 
sendCommand(0x08)#; 	  // Start from 8th Column of driver IC. This is 0th Column for OLED 
sendCommand(0x37)#; 	  // End at  (8 + 47)th column. Each Column has 2 pixels(segments)

grayH= 0xF0#;
grayL= 0x0F#;

for j in range(0,48):
	for i in range(0,96):
		sendData(0x00)