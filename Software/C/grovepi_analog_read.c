// GrovePi Example for using the analog read.
// http://dexterindustries.com/grovepi
#include "grovepi.h"
//g++ grovepi_analog_write.c grovepi.c -Wall

int main()
{
	bool success = initGrovePi(); //initialize communications w/ GrovePi
	int pin = 0; // select an analog capable pin
	int incoming; // variable to hold data for reading

	// if communication has been established
	if(success)
	{
		// continuously read data
		while(true)
		{
			// read the data
			// receives a 10-bit value which maps to
			// 0V -> VCC, where VCC is the supply voltage of GrovePi
			incoming = analogRead(pin);
			printf("[pin %d][analog read] = %d", pin, incoming);
			if(incoming == -1)
			{
				printf("IO error on I2C");
				break;
			}
		}
	}

	return 0;
}
