Grove - Gesture Sensor v1.0 Python library and examples
=======================================================
####This library is for using the Grove - Gesture Sensor v1.0(http://www.seeedstudio.com/depot/Grove-Gesture-p-2463.html)

Code derived from the basic Arduino library for the Gesture Sensor by Seeed: https://github.com/Seeed-Studio/Gesture_PAJ7620

#####Files:
* **grove_gesture_sensor.p**y: library with functions to read data from the gesture sensors
* **gesture_print.py**: This example prints the gesture on the screen when a user does an action over the sensor. Useful when testing the gesture sensor
* **gesture_value.py**: This example returns a value when a user does an action over the sensor. Useful when integrating in your own examples

#####NOTE:
* This is an I2C sensor so you can connect it to any I2C port on the GrovePi
* The gesture sensor might restart your GrovePi if you hot-plug the sensor when the GrovePi is already powered on. Please connect the sensor before powering on the GrovePi
* The sensor polls the sensor ~.1s and after reading takes ~.4s to 1s to start polling again
* The datasheet for the sensor mentions the sensing distance b/w 5 and 15 cm 
* The sensor uses IR so it would be better to keep it away from IR sources of light

######The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi

######Have a question about this library?  Ask on the forums here:  http://forum.dexterindustries.com/c/grovepi

# License

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
