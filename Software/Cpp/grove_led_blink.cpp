//
// GrovePi LED blink Example for the Grove LED Socket (http://www.seeedstudio.com/wiki/Grove_-_LED_Socket_Kit)
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

// sudo g++ -Wall grovepi.cpp grove_led_blink.cpp -o grove_led_blink.out -> without grovepicpp package installed
// sudo g++ -Wall -lgrovepicpp grove_led_blink.cpp -o grove_led_blink.out -> with grovepicpp package installed

int main()
{
	int LED_pin = 4; // Grove LED is connected to digital port D4 on the GrovePi

	try
	{
		initGrovePi(); // initialize communication w/ GrovePi
		pinMode(LED_pin, OUTPUT); // set the LED pin as OUTPUT on the GrovePi
		delay(1000); // wait 1 second

		printf("This example will blink a Grove LED connected to the GrovePi+ on the port labeled D4.\n");
		printf("If you're having trouble seeing the LED blink, be sure to check the LED connection and the port number.\n");
		printf("You may also try reversing the direction of the LED on the sensor.\n\n");
		printf("Connect the LED to the port label D4!\n");

		// do indefinitely
		while(true)
		{
			// 1 second the LED is HIGH -> ON
			digitalWrite(LED_pin, HIGH);
			printf("[pin %d][LED ON]\n", LED_pin);
			delay(1000);

			// and another second LED is LOW -> OFF
			digitalWrite(LED_pin, LOW);
			printf("[pin %d][LED OFF]\n", LED_pin);
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
