// GrovePi Example for using the digital write command
// http://dexterindustries.com/grovepi
#include "grovepi.h"
//g++ grovepi_digital_write.c grovepi.c -Wall

int main()
{
	bool success = initGrovePi(ADDRESS); // initialize communications w/ GrovePi
	int pin = 4; // select a digital pin
	int delay = 500; // measured in ms

	// if communication has been established
	if(success)
	{
		// set the pin as an OUTPUT
		pinMode(pin, OUTPUT);

		// continuously digital write
		// good LED Example
		// 0.5 seconds OFF / 0.5 seconds ON
		while(true)
		{
			printf("[pin %d][led] = ON\n", pin);
			digitalWrite(pin, HIGH);
			piSleep(delay);

			printf("[pin %d][led] = OFF\n", pin);
			digitalWrite(pin, LOW);
			piSleep(delay);
		}
	}

	return 0;
}
