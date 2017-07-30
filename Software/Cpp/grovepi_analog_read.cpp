// GrovePi Example for using the analog read.
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

// sudo g++ -Wall grovepi.cpp grovepi_analog_read.cpp -o grovepi_analog_read.out -> without grovepicpp package installed
// sudo g++ -Wall -lgrovepicpp grovepi_analog_read.cpp -o grovepi_analog_read.out -> with grovepicpp package installed

int main()
{
	int pin = 0; // we use port A0
	int incoming; // variable to hold data for reading

	try
	{
		initGrovePi(); //initialize communication w/ GrovePi

		// set the pin mode for reading
		pinMode(pin, INPUT);
		// continuously read data
		while(true)
		{
			// read the data
			// receives a 10-bit value which maps to
			// 0V -> VCC, where VCC is the supply voltage of GrovePi
			incoming = analogRead(pin);
			printf("[pin %d][analog read = %d]\n", pin, incoming);

			// wait 10 ms so we don't overflow the terminal
			delay(10);
		}
	}
	catch (I2CError &error)
	{
		printf(error.detail());

		return -1;
	}

	return 0;
}
