//
// GrovePi Example for using the Grove LED for LED Fade effect (http://www.seeedstudio.com/wiki/Grove_-_LED_Socket_Kit)
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

// sudo g++ -Wall grovepi.cpp grove_led_fade.cpp -o grove_led_fade.out -> without grovepicpp package installed
// sudo g++ -Wall -lgrovepicpp grove_led_fade.cpp -o grove_led_fade.out -> with grovepicpp package installed

int main()
{
	int LED_pin = 5; // Grove LED is connected to digital port D5 on the GrovePi
	int brigthness = 0; // initial brigthness of 0 (0 to 255)

	try
	{
		initGrovePi();
		pinMode(LED_pin, OUTPUT); // set the LED pin as OUTPUT
		delay(1000); // and wait a second

		// do indefinitely
		while(true)
		{
			// reset if above 255
			// the GrovePi has 8-bit DAC
			if(brigthness > 255)
				brigthness = 0;

			// and set the LED brigthness
			analogWrite(LED_pin, brigthness);
			float percentage_brightness = 100 * float(brigthness) / 255;
			printf("[pin %d][led brigthness = %.2f%%]\n", LED_pin, percentage_brightness);

			// increment brigthness for next iteration
			brigthness += 10;
			delay(50);
		}
	}
	catch(I2CError &error)
	{
		printf(error.detail());

		return -1;
	}

	return 0;
}
