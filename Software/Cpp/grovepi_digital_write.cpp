// GrovePi Example for using the digital write command
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
//g++ grovepi_digital_write.c grovepi.c -Wall

int main()
{
	int pin = 4; // we use port D4
	int period = 500; // measured in ms

	try
	{
		initGrovePi(); // initialize communication w/ GrovePi
		pinMode(pin, OUTPUT); // set the pin for digital writing

		// continuously digital write
		// good LED Example
		// [period] ms OFF / [period] ms ON
		while(true)
		{
			printf("[pin %d][led = ON]\n", pin);
			digitalWrite(pin, HIGH);
			delay(period);

			printf("[pin %d][led = OFF]\n", pin);
			digitalWrite(pin, LOW);
			delay(period);
		}
	}
	catch (I2CError &error)
	{
		printf(error.detail());

		return -1;
	}

	return 0;
}
