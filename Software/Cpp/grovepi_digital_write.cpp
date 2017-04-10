// GrovePi Example for using the digital write command
// http://dexterindustries.com/grovepi
#include "grovepi.h"
//g++ grovepi_digital_write.c grovepi.c -Wall

int main()
{
	bool success = initGrovePi(); // initialize communications w/ GrovePi
	int pin = 4; // select a digital pin
	int period = 500; // measured in ms

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
			delay(period);

			printf("[pin %d][led] = OFF\n", pin);
			digitalWrite(pin, LOW);
			delay(period);
		}
	}

	return 0;
}
