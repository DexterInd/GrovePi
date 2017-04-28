//
// GrovePi Example for using the Grove Button (http://www.seeedstudio.com/wiki/Grove_-_Button)
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

// sudo g++ -Wall grovepi.cpp grove_button.cpp -o grove_button.out -> without grovepicpp package installed
// sudo g++ -Wall -lgrovepicpp grove_button.cpp -o grove_button.out -> with grovepicpp package installed

int main()
{
	int button_pin = 4; // Grove Button is connected to digital port D4 on the GrovePi
	int button_state; // variable to hold the current state of the button

	try
	{
		initGrovePi(); // initialize communications w/ GrovePi
		pinMode(button_pin, INPUT); // set the button_pin (D3) as INPUT

		// do this indefinitely
		while(true)
		{
			button_state = digitalRead(button_pin); // read the button state
			printf("[pin %d][button state = ", button_pin); // and print it on the terminal screen
			if(button_state == 0)
				printf("not pressed]\n");
			else
				printf("pressed]\n");

			delay(100); // wait 100 ms for the next reading
		}
	}
	catch (I2CError &error)
	{
		printf(error.detail());

		return -1;
	}

	return 0;
}
