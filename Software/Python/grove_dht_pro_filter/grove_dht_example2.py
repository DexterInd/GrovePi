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

from grove_dht import Dht # from a custom made grovepi-based library import our needed class
from time import sleep # we need to use the sleep function to delay readings
import datetime # that's for printing the current date

# Don't forget to run it with Python 3 !!
# Don't forget to run it with Python 3 !!
# Don't forget to run it with Python 3 !!

dht_pin = 4 # use Digital Port 4 found on GrovePi
dht_sensor = Dht(dht_pin) # instantiate a dht class with the appropriate pin

dht_sensor.start() # start collecting from the DHT sensor

try:
    # do this indefinitely
    while True:
        string = '[' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ']' # keep a track of the current time

        temperature, humidity = dht_sensor.feedMe() # try to read values

        # if any of the read values is a None type, then it means there're no available values
        if not temperature is None:
            string += '[temperature = {:.01f}][humidity = {:.01f}]'.format(temperature, humidity)
        else:
            string += '[waiting for buffer to fill]'

        print(string)
        sleep(0.8) # wait around 800 ms before the next iteration

# when pressing CTRL-C
except KeyboardInterrupt:
    dht_sensor.stop() # stop gathering data
