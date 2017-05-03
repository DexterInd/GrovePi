// GrovePi Example for using the analog write
// http://dexterindustries.com/grovepi

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
using namespace GrovePi;

// sudo g++ -Wall grovepi.cpp grovepi_analog_write.cpp -o grovepi_analog_write.out -> without grovepicpp package installed
// sudo g++ -Wall -lgrovepicpp grovepi_analog_write.cpp -o grovepi_analog_write.out -> with grovepicpp package installed

int main()
{
	int pin = 3; // we use port D3

	// for direction = HIGH the value we write increases with each step
	// for direction = LOW the value we write decreases with each step
	int direction = HIGH;
	int increment_value = 3; // step increase for PWN function
	int final_value = 0; // variable to hold to value to write to GrovePi

	try
	{
		initGrovePi(); // initialize communication w/ GrovePi
		pinMode(pin, OUTPUT); // set the pin mode for writing

		// continuously do this
		while(true)
		{
			// iterate the whole range of values
			// 0 -> 255 maps to 0V -> VCC, where VCC is the supply voltage on GrovePi
			//
			// since we're using the a PWM function
			// we have a duty cycle that goes from 0% to 100% of VCC voltage
			// with an increase/decrease of voltage of 100 * increment_value / 256 = 0.39%  / increment
			//
			// google what a PWM wave is
			for(int value = 0; value <= 255; value += increment_value)
			{
				final_value = 0; // reset it
				if(direction == HIGH)
					// if direction == HIGH then let the final_value take ascending values
					final_value = value;
				else if(direction == LOW)
					// if direction == LOW then let the final_value take descending values
					final_value = 255 - value;

				printf("[pin %d][analog write = %d]\n", pin, final_value);
				analogWrite(pin, final_value);
				delay(5); // wait 5 ms for the next change in pin value
			}

			// if increment_value = HIGH then change it to increment_value = LOW
			// if increment_value = LOW then change it to increment_value = HIGH
			direction = (direction == HIGH) ? LOW : HIGH;
		}
	}
	catch (I2CError &error)
	{
		printf(error.detail());

		return -1;
	}

	return 0;
}
