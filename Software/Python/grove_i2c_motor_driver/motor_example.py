#!/usr/bin/env python
#
# GrovePi Example for using the Grove - I2C Motor Driver(http://www.seeedstudio.com/depot/Grove-I2C-Motor-Driver-p-907.html)
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://forum.dexterindustries.com/c/grovepi
#
# NOTE:
# 	* Refer to the wiki to make sure that the address is correct: http://www.seeedstudio.com/wiki/Grove_-_I2C_Motor_Driver_V1.3 
#	* The I2C motor driver is very sensitive to the commands being sent to it
#	* Do not run i2cdetect or send a wrong command to it, the motor driver will stop working and also pull down the I2C clock line, which makes the GrovePi or any other device to stop working too
#	*Press reset when if you keep getting errors
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

import grove_i2c_motor_driver
import time

try:
	# You can initialize with a different address too: grove_i2c_motor_driver.motor_driver(address=0x0a)
	m= grove_i2c_motor_driver.motor_driver()

	#FORWARD
	print("Forward")
	m.MotorSpeedSetAB(100,100)	#defines the speed of motor 1 and motor 2;
	m.MotorDirectionSet(0b1010)	#"0b1010" defines the output polarity, "10" means the M+ is "positive" while the M- is "negtive"
	time.sleep(2)

	#BACK
	print("Back")
	m.MotorSpeedSetAB(100,100)
	m.MotorDirectionSet(0b0101)	#0b0101  Rotating in the opposite direction
	time.sleep(2)

	#STOP
	print("Stop")
	m.MotorSpeedSetAB(0,0)
	time.sleep(1)

	#Increase speed
	for i in range (100):
		print("Speed:",i)
		m.MotorSpeedSetAB(i,i)
		time.sleep(.02)
		
	print("Stop")
	m.MotorSpeedSetAB(0,0)	
	
except IOError:
	print("Unable to find the motor driver, check the addrees and press reset on the motor driver and try again")
	