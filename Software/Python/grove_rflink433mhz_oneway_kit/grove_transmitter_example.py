#!/usr/bin/env python3
#
# GrovePi Example for using the Grove - LCD RGB Backlight without erasing the screen(http://www.seeedstudio.com/wiki/Grove_-_LCD_RGB_Backlight)
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

import grove_rflink433mhz
from time import sleep
import sys

# Don't forget to run it with Python 3 !!
# Don't forget to run it with Python 3 !!
# Don't forget to run it with Python 3 !!

# in order to get a feedback of what this example does
# please use another setup consisted of a raspberry + receiver
# to print out the transmitted data -> use the other example program for it

def Main():
    # instantiate a RFLinker object
    # default arguments are
    # port = '/dev/ttyS0' -> you've got only one on each raspberry
    # chunk_size = 32 -> the max number of data bytes you can send per fragment - you can ignore it
    # max_bad_readings = 32 -> the number of bad characters read before giving up on a read operation
    # keep in mind that there is environment pollution, so the RF module will get many fake 'transmissions'
    transmitter = grove_rflink433mhz.RFLinker()
    # the message we want to broadcast
    message_to_broadcast = "This is a RFLink test"

    # and broadcast it indefinitely
    while True:
        transmitter.writeMessage(message_to_broadcast)

        print('[message sent][{}]'.format(message_to_broadcast))
        # the delay is not necessary for the transmission of data
        # but for not overflowing the terminal
        sleep(0.02)

if __name__ == "__main__":
    try:
        # it's the above function we call
        Main()

    # in case CTRL-C / CTRL-D keys are pressed (or anything else that might interrupt)
    except KeyboardInterrupt:
        print('[Keyboard interrupted]')
        sys.exit(0)
