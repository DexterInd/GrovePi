//
// GrovePi Example for using the Grove Relay (http://www.seeedstudio.com/wiki/Grove_-_Relay)
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

// sudo g++ -Wall grovepi.cpp grove_relay.cpp -o grove_relay.out -> without grovepicpp package installed
// sudo g++ -Wall -lgrovepicpp grove_relay.cpp -o grove_relay.out -> with grovepicpp package installed

int main()
{
	int relay_pin = 4; // Grove Relay is connected to digital port D4 on the GrovePi

	try
	{
		initGrovePi(); // initialize communication with the GrovePi
		pinMode(relay_pin, OUTPUT); // set the relay's pin as OUTPUT

		// do this indefinitely
		while(true)
		{
			// turn it ON
			digitalWrite(relay_pin, HIGH);
			printf("[pin %d][relay ON]\n", relay_pin);

			// for 5 seconds
			delay(5000);

			// and turn it OFF
			digitalWrite(relay_pin, LOW);
			printf("[pin %d][relay OFF]\n", relay_pin);

			// for another 5 seconds
			delay(5000);
			// and repeat
		}
	}
	catch(I2CError &error)
	{
		printf(error.detail());

		return -1;
	}

	return 0;
}
