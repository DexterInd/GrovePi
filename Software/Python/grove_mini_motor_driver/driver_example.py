#!/usr/bin/env python3
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://forum.dexterindustries.com/c/grovepi
#
'''
## License

The MIT License (MIT)

GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
Copyright (C) 2017  Dexter Industries

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

from grove_mini_motor_driver import MiniMotorDriver
from grove_mini_motor_driver import left_channel, right_channel
from time import sleep
import sys

# if you use the incorporated feedbacker (aka setDisplayFaults)
# whenever there's a shortage of current or if the motors stalls
# it appears on the screen as a warning
#
# Please take a look in the terminal_log_example.txt to get a feeling
# of what this program outputs
#
# Here is some fault feedback:
#
# [04-Apr-2017 19:06:08.188770][left motor warning][undervoltage lockout]
# [04-Apr-2017 19:06:08.190704][right motor warning][undervoltage lockout]
# [04-Apr-2017 19:21:17.990704][right motor warning][overcurrent event]
# [04-Apr-2017 19:23:11.768320][right motor warning][extended current limit event]
# [04-Apr-2017 19:25:08.330140][right motor warning][overtemperature condition]
# [04-Apr-2017 19:38:54.781218][right motor warning][unknown condition]

# Don't forget to run it with Python 3 !!
# Don't forget to run it with Python 3 !!
# Don't forget to run it with Python 3 !!


def Main():
    # initialize an object of the motor driver class
    # with the appropiate channel address
    # we can also add a 3rd argument which is a SMBus objeclt
    # in case we don't want to let the class instantiate it
    driver = MiniMotorDriver(left_channel, right_channel)

    # enable display feedback/output of motors status
    # alternatively we can use driver.setDisplayFaults(False) to disable it
    driver.setDisplayFaults()

    # increase the power to the motors from 0% -> 100% in 5 seconds
    # motors rotate in tandem
    for percent in range(101):
        driver.moveForward(percent)
        sleep(0.05)
    # stay at 100% power for 2 seconds
    sleep(2)

    # and then move backwards at 50% thrust for another 2 seconds
    driver.moveBackwards(50)
    sleep(2)

    # stop the motors immediately -> driver opposes an electromotive force
    # in order to stop the motors faster rather then cutting the power
    driver.stopMotors()
    # stay off for 1 second
    sleep(1)

    # and then set the right motor to FORWARD direction at 70% thrust
    driver.setRightMotor('FORWARD', 70)
    # and keep this going for 5 seconds
    sleep(5)

    # while it's spinning, completely reverse the thrust
    # for another 5 seconds
    driver.setRightMotor('REVERSE', 70)
    sleep(5)

    # then set the motors rotate in opposing directions
    # such a command would make a GopiGo rotate in the same spot
    # do this for one second
    driver.setRightMotor('FORWARD', 50)
    driver.setLeftMotor('REVERSE', 50)
    sleep(1)

    # and disable motors
    # it's different then the stopMotors() function
    # because it just cuts power definitely and
    # puts the motor driver in a low-power state
    driver.disableMotors()

if __name__ == "__main__":
    try:
        # it's the above function we call
        Main()

    # in case CTRL-C / CTRL-D keys are pressed (or anything else that might interrupt)
    except KeyboardInterrupt:
        print('[Keyboard interrupted]')
        sys.exit(0)

    # in case there's an IO error aka I2C
    except IOError:
        print('[IO Error]')
        sys.exit(0)
