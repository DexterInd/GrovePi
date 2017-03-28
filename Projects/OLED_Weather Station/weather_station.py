# Adapted from home_temp_hum_display.py
'''

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

from grovepi import *
from grove_oled import *

import threading

dht_sensor_port = 7        # Connect the DHt sensor to port 7

#Start and initialize the OLED
oled_init()
oled_clearDisplay()
oled_setNormalDisplay()
oled_setVerticalMode()
time.sleep(.1)


def get_outside_weather(location='Bucharest,ro'):
    import pyowm  # Do a 'sudo pip install pyowm' to get this module

    owm = pyowm.OWM()

    #forecast = owm.daily_forecast(location)

    observation = owm.weather_at_place(location)
    weather = observation.get_weather()

    return weather


def update_outside_weather():
    # This uses OpenWeatherMap via the PyOWM module;
    # pywom module needs to be installed via pip,
    # see https://github.com/csparpa/pyowm
    weather = get_outside_weather()
    # by default location is Bucharest,ro; change it to your own

    oled_setTextXY(5, 1)
    oled_putString("OUTSIDE")

    oled_setTextXY(7, 0)
    oled_putString("Temp:")
    oled_putString(str(weather.get_temperature("celsius")['temp']) + "C")

    oled_setTextXY(8, 0)
    oled_putString("Hum :")
    oled_putString(str(weather.get_humidity()) + "%")

    oled_setTextXY(9, 0)
    oled_putString("Rain:")

    rain = weather.get_rain()
    if len(rain) > 0:
        pass
    else:
        oled_putString("0%")

    print(("Weather: ", weather.get_temperature("celsius")))
    print(("Humidity: ", weather.get_humidity()))

while True:
    try:
        # Get the temperature and Humidity from the DHT sensor
        [temp, hum] = dht(dht_sensor_port, 1)
        print(("Temp =", temp, "C\tHumidity =", hum, "%"))
        t = str(temp)
        h = str(hum)

        #outside_thread = threading.Thread(target=update_outside_weather)
        #outside_thread.start()

        oled_setTextXY(0, 1)       # Print "INSIDE" at line 1
        oled_putString("INSIDE")

        oled_setTextXY(2, 0)       # Print "TEMP" and the temperature in line 3
        oled_putString("Temp:")
        oled_putString(t + "C")

        oled_setTextXY(3, 0)       # Print "HUM :" and the humidity in line 4
        oled_putString("Hum :")
        oled_putString(h + "%")

        #outside_thread.join()
        update_outside_weather()

    except (IOError, TypeError, Exception) as e:
        print(("Error:" + str(e)))
    finally:
        #outside_thread.join()
        pass
