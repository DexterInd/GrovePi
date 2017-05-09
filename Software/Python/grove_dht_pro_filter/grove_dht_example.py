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

from grove_dht import Dht
import signal
import sys

# Don't forget to run it with Python 3 !!
# Don't forget to run it with Python 3 !!
# Don't forget to run it with Python 3 !!

# Please read the source file(s) for more explanations
# You'll get to see that the source file(s) are explained through comments

dht = Dht()

def signal_handler(signal, frame):
    global dht
    dht.stop()

def callbackFunc():
    global dht
    print(dht)

def Main():
    print("[program is running][please wait]")

    global dht
    digital_port = 4

    # set the digital port for the DHT sensor
    dht.setDhtPin(digital_port)
    # using the blue kind of sensor
    # there's also the white one which can be set by calling [dht.setAsWhiteSensor()] function
    dht.setAsBlueSensor()
    # sets the period in seconds
    # after every each period, the algorithm filters the values it recorded in the buffer
    # and then it calls the callback function (if provided)
    dht.setRefreshPeriod(12)
    # set the filtering aggresiveness
    # the smaller is the parameter, the more aggresive is the filtering process
    # it's vice versa with higher-valued parameters
    # by default, it's set at 2.0
    dht.setFilteringAggresiveness(2.1)
    # whenever we get a new filtered data, it calls the argument-passed function
    # you can also provide a variable length parameters to the callback function
    # through the same function
    dht.setCallbackFunction(callbackFunc)

    # start the thread for gathering data
    dht.start()

    # if you want to stop the thread just
    # call dht.stop() and you're done


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    Main()
