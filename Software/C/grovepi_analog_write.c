// GrovePi Example for using the analog write
// http://dexterindustries.com/grovepi
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
				piSleep(10); // wait 10 ms
			}
		}
	}

	return 0;
}
