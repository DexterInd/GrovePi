// GrovePi Example for using the digital read command
// http://dexterindustries.com/grovepi
#include "grovepi.h"
//g++ grovepi_digital_read.c grovepi.c -Wall

int main()
{
	bool success = initGrovePi(); // initialize communications w/ GrovePi
	int pin = 4; // select a digital pin
	int state; // variable to hold the ON/OFF state


	if(success)
	{
		// set the pin as an INPUT port
		pinMode(pin, INPUT);
		// continuously read the data
		while(true)
		{
			// read the data
			state = digitalRead(pin);
			printf("[pin %d][digital read] = ", pin);
			if(state == 0)
				printf("LOW\n");
			else
				printf("HIGH\n");

			// wait 50 ms so that the program doesn't run too fast
			piSleep(50);
		}
	}

	return 0;
}
