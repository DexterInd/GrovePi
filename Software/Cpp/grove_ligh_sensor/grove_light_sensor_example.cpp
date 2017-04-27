//
// GrovePi Example for using the Grove Light Sensor and the LED together to turn the LED On and OFF if the background light is greater than a threshold.
// Modules:
//      http://www.seeedstudio.com/wiki/Grove_-_Light_Sensor
//      http://www.seeedstudio.com/wiki/Grove_-_LED_Socket_Kit
//
// The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
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

	int light_sensor_pin = 0; // analog port A0 for the Grove Light Sensor
	int LED_pin = 4; // digital port D4 for the Grove LED
	int threshold = 10; // threshold value in kOhm for the Grove Light Sensor
	int sensor_value; // variable to hold the Grove Light Sensor value
	float resistance; // variable to hold the Grove Light Sensor's resistance value

	// set the LED & Light pins accordingly
	pinMode(light_sensor_pin, INPUT);
	pinMode(LED_pin, OUTPUT);

	// start reading the value on the Light Sensor
	sensor_value = analogRead(light_sensor_pin);
	// while I2C error stays below the threshold
	while(current_retries < max_retries)
	{
		// if error occured during reading
		if(sensor_value == -1)
		{
			// then increase the retry counter
			current_retries += 1;
		}
		else
		{
			// otherwise reset the counter
			current_retries = 0;
			// calculate the resistance
			resistance = (float)(1023 - sensor_value) * 10 / sensor_value;

			// check if the resistance gets beyond the threshold
			// value in kOhm (check how a light sensor works)
			// and turn ON/OFF the LED on the associated pin accordingly
			if(resistance > threshold)
				digitalWrite(LED_pin, HIGH);
			else
				digitalWrite(LED_pin, LOW);

			// and finally print the
			printf("[sensor value = %d][resistance = %.2f]\n", sensor_value, resistance);
		}

		// wait half a second for the next reading
		delay(500);
		sensor_value = analogRead(light_sensor_pin);
	}

	return 0;
}
