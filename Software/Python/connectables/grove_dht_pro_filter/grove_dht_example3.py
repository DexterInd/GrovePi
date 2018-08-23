#!/usr/bin/env python3
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
# Connect the Grove DHT Sensor (Blue One) to Port 4 in this example.
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
# Source file(s) are more comprehensive

dht_sensor = Dht()

def signal_handler(signal, frame):
    global dht_sensor
    dht_sensor.stop()

def callbackFunc():
    global dht_sensor
    print(dht_sensor)

def Main():
    print("[program is running][please wait]")

    global dht_sensor
    digital_port = 4

    # set the digital port for the DHT sensor
    dht_sensor.setDhtPin(digital_port)
    # using the blue kind of sensor
    # there's also the white one which can be set by calling [dht.setAsWhiteSensor()] function
    dht_sensor.setAsBlueSensor()
    # specifies for how long we record data before we filter it
    # it's better to have larger periods of time,
    # because the statistical algorithm has a vaster pool of values
    dht_sensor.setRefreshPeriod(12)
    # the bigger is the filtering factor (as in the filtering aggresiveness)
    # the less strict is the algorithm when it comes to filtering
    # it's also valid vice-versa
    # the factor must be greater than 0
    # it's recommended to leave its default value unless there is a better reason
    dht_sensor.setFilteringAggresiveness(2.1)
    # every time the Dht object loads new filtered data inside the buffer
    # a callback is what it follows
    dht_sensor.setCallbackFunction(callbackFunc)

    # start the thread for gathering data
    dht_sensor.start()

    # if you want to stop the thread just
    # call dht.stop() and you're done


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    Main()
