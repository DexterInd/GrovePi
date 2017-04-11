// GrovePi Example for using the digital read command
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
//g++ grovepi_digital_read.c grovepi.c -Wall

int main()
{
	bool success = initGrovePi(); // initialize communications w/ GrovePi
	int pin = 4; // select a digital pin
	int state; // variable to hold the ON/OFF state


	if(success)
	{
		// set the pin as an INPUT port
		pinMode(pin, INPUT);
		// continuously read the data
		while(true)
		{
			// read the data
			state = digitalRead(pin);
			printf("[pin %d][digital read] = ", pin);
			if(state == 0)
				printf("LOW\n");
			else
				printf("HIGH\n");

			// wait 50 ms so that the program doesn't run too fast
			delay(50);
		}
	}

	return 0;
}
