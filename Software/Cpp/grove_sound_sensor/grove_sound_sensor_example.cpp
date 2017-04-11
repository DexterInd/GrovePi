//
// GrovePi Example for using the Grove Sound Sensor and the Grove LED
//
// The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
//
// Modules:
//	 http://www.seeedstudio.com/wiki/Grove_-_Sound_Sensor
//	 http://www.seeedstudio.com/wiki/Grove_-_LED_Socket_Kit
//
// Have a question about this example?  Ask on the forums here:  http://forum.dexterindustries.com/c/grovepi
//
/*
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
*/

#include "grovepi.h"

int main()
{
	int current_retries = 0; // current number of I2C errors encountered
	int max_retries = 5; // maximum number of consecutive I2C errors

	int sound_sensor_pin = 0; // analog port A0 for the Grove Sound Sensor
	int LED_pin = 5; // digital port D5 for the Grove LED
	int threshold_value = 400; // threshold value for the sound levels (values from 0 -> 1023)
	int sensor_value; // variable to hold the Sound Sensor's value

	// set the LED & Sound pins accordingly
	pinMode(sound_sensor_pin, INPUT);
	pinMode(LED_pin, OUTPUT);


	// start reading the value on the Sound sensor
	sensor_value = analogRead(sound_sensor_pin);
	// while I2C error threshold not hit
	while(current_retries < max_retries)
	{
		if(sensor_value == -1)
		{
			current_retries += 1;
		}
		else
		{
			// reset the counter since we care
			// about the consecutives
			current_retries = 0;
			// check whether we turn the LED ON or OFF
			// based on the threshold value
			if(sensor_value > threshold_value)
				digitalWrite(LED_pin, HIGH);
			else
				digitalWrite(LED_pin, LOW);

			// and print the sensor value onto the terminal
			printf("[sensor value = %d]\n", sensor_value);
		}

		// and wait 500 ms for the next reading
		delay(500);
		sensor_value = analogRead(sound_sensor_pin);
	}

	printf("[I2C errors threshold hit]\n");

	return 0;
}
