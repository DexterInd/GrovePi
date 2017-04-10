#include "grove_rgb_lcd.h"
#include "grovepi.h"
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
