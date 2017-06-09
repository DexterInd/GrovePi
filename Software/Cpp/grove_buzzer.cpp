//
// GrovePi Example for using the Grove Buzzer (http://www.seeedstudio.com/wiki/Grove_-_Buzzer)
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
using namespace GrovePi;

// sudo g++ -Wall grovepi.cpp grove_buzzer.cpp -o grove_buzzer.out -> without grovepicpp package installed
// sudo g++ -Wall -lgrovepicpp grove_buzzer.cpp -o grove_buzzer.out -> with grovepicpp package installed

int main()
{
	int buzzer_pin = 8; // Grove Buzzer is connected to digital port D8 on the GrovePi

	try
	{
		initGrovePi(); // initialize communication with the GrovePi
		pinMode(buzzer_pin, OUTPUT); // set the buzzer_pin as OUTPUT (we have a buzzer)

		// do indefinitely
		while(true)
		{
			// turn ON the buzzer for 1000 ms (1 sec)
			// and put the state on the screen
			digitalWrite(buzzer_pin, HIGH);
			printf("[pin %d][buzzer ON]\n", buzzer_pin);
			delay(1000);

			// and then OFF for another 1000 ms (1 sec)
			// and put the state on the screen
			digitalWrite(buzzer_pin, LOW);
			printf("[pin %d][buzzer OFF]\n", buzzer_pin);
			delay(1000);
		}
	}
	catch(I2CError &error)
	{
		printf(error.detail());

		return -1;
	}

	return 0;
}
