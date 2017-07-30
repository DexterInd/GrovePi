#!/usr/bin/env python3
# -*- coding: utf8 -*-
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

import grove_hightemperature_sensor as grovepi # our library
from time import sleep # and for the sleep function
import sys # we need this for the exception throwing stuff

# Don't forget to run it with Python 3 !!
# Don't forget to run it with Python 3 !!
# Don't forget to run it with Python 3 !!

def Main():
    room_temperature_pin = 15 # this is equal to A1
    probe_temperature_pin = 14 # this is equal to A0
    # so you have to connect the sensor to A0 port

    # instatiate a HighTemperatureSensor object
    sensor = grovepi.HighTemperatureSensor(room_temperature_pin, probe_temperature_pin)

    # and do this indefinitely
    while True:
        # read the room temperature
        room_temperature = sensor.getRoomTemperature()
        # and also what's important to us: the temperature at the tip of the K-Type sensor
        probe_temperature = sensor.getProbeTemperature()

        # print it in a fashionable way
        print('[room temperature: {:5.2f}°C][probe temperature: {:5.2f}°C]'.format(room_temperature, probe_temperature))
        # and wait for 250 ms before taking another measurement - so we don't overflow the terminal
        sleep(0.25)


if __name__ == "__main__":
    try:
        Main()

    # in case CTRL-C / CTRL-D keys are pressed (or anything else that might interrupt)
    except KeyboardInterrupt:
        print('[Keyboard interrupted]')
        sys.exit(0)

    # in case there's an IO error aka I2C
    except IOError:
        print('[IO Error]')
        sys.exit(0)

    # in case we have a math error (like division by 0 - can happen depending on the read values)
    # or if the values exceed a certain threshold
    # experiment and you'll see
    except ValueError as e:
        print('[{}]'.format(str(e)))
        sys.exit(0)
