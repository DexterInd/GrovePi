import smbus
import time
import grovepi
# for RPI version 1, use "bus = smbus.SMBus(0)"
bus = smbus.SMBus(0)

# This is the address we setup in the Arduino Program
address = 0x04

def writeNumber(value):
    bus.write_byte(address, value)
    # bus.write_byte_data(address, 0, value)
    return -1

def readNumber():
    number = bus.read_byte(address)
    # number = bus.read_byte_data(address, 1)
    return number

# grovepi.pinMode(7,"INPUT")
time.sleep(1)
i = 0
while True:
    print grovepi.analogRead(0)
    time.sleep(1)
