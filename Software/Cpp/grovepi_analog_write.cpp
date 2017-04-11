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
//g++ grovepi_analog_write.c grovepi.c -Wall

int main()
{
	bool success = initGrovePi(); // initialize communications w/ GrovePi
	int pin = 3; // select an analog capable pin

	if(success)
	{
		// continuously write data
		while(true)
		{
			// iterate the whole range of values
			// 0 -> 255 maps to 0V -> VCC, where VCC is the supply voltage on GrovePi
			for(int value = 0; value < 256; value++)
			{
				printf("[pin %d][analog write] = %d\n", pin, value);
				analogWrite(pin, value);
				delay(50); // wait 10 ms
			}
		}
	}

	return 0;
}
