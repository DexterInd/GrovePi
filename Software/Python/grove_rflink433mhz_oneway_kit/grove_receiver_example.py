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

import grove_rflink433mhz
import sys

# Don't forget to run it with Python 3 !!
# Don't forget to run it with Python 3 !!
# Don't forget to run it with Python 3 !!

def Main():
    # instantiate a RFLinker object
    # default arguments are
    # port = '/dev/ttyS0' -> you've got only one on each raspberry
    # chunk_size = 32 -> the max number of data bytes you can send per fragment - you can ignore it
    # max_bad_readings = 32 -> the number of bad characters read before giving up on a read operation
    # keep in mind that there is environment pollution, so the RF module will get many fake 'transmissions'
    receiver = grove_rflink433mhz.RFLinker()
    message_received = ""

    # do this indefinitely
    while True:
        # receive the message
        # readMessage takes a default argument
        # called retries = 20
        # it specifies how many times it tries to read consistent data before giving up
        # you should not modify it unless you know what you're doing and provided you also
        # modify the chunk_size for the transmitter
        message_received = receiver.readMessage()
        if len(message_received) > 0:
            # if the string has something then print it
            print('[message received][{}]'.format(message_received))
        else:
            print("[message_received][none or couldn't parse it]")


if __name__ == "__main__":
    try:
        # it's the above function we call
        Main()

    # in case CTRL-C / CTRL-D keys are pressed (or anything else that might interrupt)
    except KeyboardInterrupt:
        print('[Keyboard interrupted]')
        sys.exit(0)
