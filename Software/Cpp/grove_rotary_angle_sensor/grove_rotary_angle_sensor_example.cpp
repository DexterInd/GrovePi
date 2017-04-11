// GrovePi Example for using the Grove Rotary Angle Sensor (Potentiometer) and the Grove LED to create LED sweep
//
// Modules:
//	 http://www.seeedstudio.com/wiki/Grove_-_Rotary_Angle_Sensor
//	 http://www.seeedstudio.com/wiki/Grove_-_LED_Socket_Kit
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

	int potentiometer_pin = 0; // potentiometer is connected to A0 port
	int LED_pin = 5; // potentiometer is connected to D5 port

	int adc_ref = 5; // reference voltage of ADC is 5V
	int grove_ref_vcc = 5; // Grove's reference voltage is 5V, regularly
	int full_angle = 300; // max turning angle for the potentiomater (almost a complete turn)

	// start reading potentiometer's values
	int sensor_value = analogRead(potentiometer_pin);
	// as long as the I2C errors don't get over a certain threshold
	while(current_retries < max_retries)
	{
		// check if there's an error on the sensor
		if(sensor_value == -1)
		{
			// and if so increase the number of retries
			current_retries += 1;
		}
		else
		{
			// otherwise reset the counter
			// because we only care of the consecutives
			current_retries = 0;

			// calculate voltage
			float voltage = (float)(sensor_value) * adc_ref / 1023;

			// calculate rotation in degrees (0 to 300)
			float degrees = voltage * full_angle / grove_ref_vcc;

			// and calculate brightness for the LED
			// basically we map values 0->300 to 0->255
			int brightness = int(degrees / full_angle * 255);

			// and give a PWM output to the LED
			analogWrite(LED_pin, brightness);

			// and display status data onto the terminal
			printf("[sensor value = %d][voltage = %.2f][degrees = %.1f][brightness = %d]\n",
			       sensor_value, voltage, degrees, brightness);
		}

		// wait 20 ms for the next reading
		// this equates to a rate of 50Hz
		// so there are 50 reads / second -> more than enough
		delay(20);
		sensor_value = analogRead(potentiometer_pin);
	}

	return 0;
}
