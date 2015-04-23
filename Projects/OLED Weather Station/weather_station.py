# Adapted from home_temp_hum_display.py

from grovepi import *
from grove_oled import *

import threading
import time
import sys
from subprocess import call

dht_sensor_port = 7        # Connect the DHt sensor to port 7


# Start and initialize the OLED
def oled_reset():
    oled_init()
    oled_clearDisplay()
    oled_setNormalDisplay()
    oled_setVerticalMode()
    time.sleep(.1)

oled_reset()

# Button on D3 port
button = 3
pinMode(button, "INPUT")

# Are in shutdown mode?
shutdown = False


def poll_shutdown_button():
    global shutdown

    buttonOut = digitalRead(button)
    if buttonOut == 1:
        shutdown = True

        call(["shutdown -r now"])  # we already have sudo, right?
        sys.exit(0)

import pyowm  # Do a 'sudo pip install pyowm' to get this module
weather_data = None
weather_thread_running = True
owm = pyowm.OWM()


# by default location is Bucharest,ro; change it to your own
def get_outside_weather(location="Bucharest,ro"):
    # This uses OpenWeatherMap via the PyOWM module;
    # pywom module needs to be installed via pip,
    # see https://github.com/csparpa/pyowm

    global weather_thread_running
    global owm
    while weather_thread_running:
        #forecast = owm.daily_forecast(location)

        observation = owm.weather_at_place(location)
        weather = observation.get_weather()

        global weather_data
        weather_data = {}
        weather_data['temp'] = str(weather.get_temperature("celsius")['temp'])
        weather_data['hum'] = str(weather.get_humidity())
        weather_data['rain'] = weather.get_rain()


def update_outside_weather():
    global weather_data

    oled_setTextXY(5, 1)
    oled_putString("OUTSIDE")

    oled_setTextXY(7, 0)
    oled_putString("Temp: ")
    oled_putString(weather_data['temp'] + "C")

    oled_setTextXY(8, 0)
    oled_putString("Hum: ")
    oled_putString(weather_data['hum'] + "%")

    oled_setTextXY(9, 0)
    oled_putString("Rain(3h): ")

    rain = weather_data['rain']
    if len(rain) > 0:
        vol_rain = rain['3h']
        print(rain)
        oled_putString(str(vol_rain) + "mm")
    else:
        oled_putString("0mm")

    print(("Weather: ", weather.get_temperature("celsius")))
    print(("Humidity: ", weather.get_humidity()))


def main_loop():
    try:
        owmThread = threading.Thread(target=get_outside_weather)
        owmThread.start()
    except:
        print("Now THAT is unexpected: could not start the button thread")

    print("Starting loop. Do a CTRL+C to halt")
    while True:
        try:
            poll_shutdown_button()

            if shutdown:
                oled_reset()

                oled_setTextXY(0, 1)
                oled_putString("GOODBYE!")
                break

            # Get the temperature and Humidity from the DHT sensor
            [temp, hum] = dht(dht_sensor_port, 1)
            print(("Temp =", temp, "C\tHumidity =", hum, "%"))
            t = str(temp)
            h = str(hum)

            #outside_thread = threading.Thread(target=update_outside_weather)
            #outside_thread.start()

            oled_setTextXY(0, 1)       # Print "INSIDE" at line 1
            oled_putString("INSIDE")

            oled_setTextXY(2, 0)   # Print "TEMP" and the temperature on line 3
            oled_putString("Temp: ")
            oled_putString(t + "C")

            oled_setTextXY(3, 0)   # Print "HUM :" and the humidity on line 4
            oled_putString("Hum: ")
            oled_putString(h + "%")

            #outside_thread.join()
            global weather_data
            if weather_data:
                update_outside_weather()

            time.sleep(.5)  # Let's not totally kill the CPU here
        except KeyboardInterrupt:
            global weather_thread_running
            weather_thread_running = False  # kill thread
            break
        except (IOError, TypeError, Exception) as e:
            print(("Error:" + str(e)))
        finally:
            pass


if __name__ == '__main__':
    main_loop()
