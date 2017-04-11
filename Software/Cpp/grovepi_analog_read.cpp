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
//g++ grovepi_analog_write.c grovepi.c -Wall

int main()
{
	bool success = initGrovePi(); //initialize communications w/ GrovePi
	int pin = 0; // select an analog capable pin
	int incoming; // variable to hold data for reading

	// if communication has been established
	if(success)
	{
		// continuously read data
		while(true)
		{
			// read the data
			// receives a 10-bit value which maps to
			// 0V -> VCC, where VCC is the supply voltage of GrovePi
			incoming = analogRead(pin);
			printf("[pin %d][analog read] = %d\n", pin, incoming);
			if(incoming == -1)
			{
				printf("IO error on I2C\n");
				break;
			}
		}
	}

	return 0;
}
