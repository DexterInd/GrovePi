//
// GrovePi Example for using the Grove - LCD RGB Backlight (http://www.seeedstudio.com/wiki/Grove_-_LCD_RGB_Backlight)
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
#include "grove_rgb_lcd.h"
#include <stdlib.h>
#include <stdio.h>

int main()
{
	GroveLCD lcd; // initialize new Grove LCD RGB device
	int max_retries = 5;
	int current_retries = 0;
	bool job_done = false;

	while(job_done == false && current_retries < max_retries)
	{

		try{
			// set/reset the counter
			current_retries = 0;

			// connect to the i2c-line
			lcd.connect();

			// set text and RGB color on the LCD
			lcd.setText("Hello world\nThis is an LCD test");
			lcd.setRGB(0, 128, 64);

			// continuously change color for roughly 2.5 seconds
			for(int value = 0; value < 256; value++)
			{
				lcd.setRGB(value, 255 - value, 0);
				delay(10);
			}
			// set final color
			lcd.setRGB(0, 255, 0);

			// and display a last minute text
			lcd.setText("Bye bye, this should wrap onto the next line");

			job_done = true;
		}
		catch (I2CError &error) {

			// if any connection errors arise
			// throw runtime exception

			if(current_retries < max_retries)
			{
				// if number of max retries haven't reached the threshold
				// then retry again to communicate
				current_retries += 1;
				continue;
			}
			else
				// if connection can't be established
				// print the error (w/ details about the location of it)
				printf(error.detailError());
		}
	}

	return 0;
}
