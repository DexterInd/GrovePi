rove - RTC DS1307 v1.1 Python library and examples
=======================================================
####This library is for using the Grove - RTC DS1307 v1.1(http://wiki.seeedstudio.com/wiki/Grove_-_RTC)

Code derived from SwitchDoc Labs github repository: https://github.com/switchdoclabs/RTC_SDL_DS1307

#####Files:
* **grove_i2c_rtc_ds1307.p**y: library with functions to set and read the date and time from RTC DS1307
* **rtc_ds1307.py**: This example sets the clock of DS1307 and prints value of all the clocks(Raspberry Pi and DS1307) every 10 seconds. 

#####NOTE:
* This is an I2C sensor so you can connect it to any I2C port on the GrovePi
* Please have the sensor powered by a battery before connecting to any of the I2C port on the GrovePi.
* There are two ways to write the time to DS1307.
* One is to write the time of Raspberry Pi, which is done by default in the example.
* The other way is to write a user prefered date and time, this can be done by uncommenting lines 54-56.

######The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi

######Have a question about this library?  Ask on the forums here:  http://www.dexterindustries.com/forum/?forum=grovepi

# License

The MIT License (MIT)

GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
Copyright (C) 2015  Dexter Industries

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
