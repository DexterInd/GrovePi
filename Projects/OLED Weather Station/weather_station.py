# Adapted from home_temp_hum_display.py
'''
## License
 GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
 Copyright (C) 2015  Dexter Industries

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/gpl-3.0.txt>.
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
