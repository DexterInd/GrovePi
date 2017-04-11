// GrovePi Example for using the digital write command
// http://dexterindustries.com/grovepi
#include "grovepi.h"
//g++ grovepi_us_read.c grovepi.c -Wall

int main()
{
	bool success = initGrovePi();
	int pin = 4;
	int incoming; // variable to hold the data

	// if communication has been established
	if(success)
	{
		while(true)
		{
			incoming = ultrasonicRead(pin);
			printf("[pin %d][ultrasonic read] = %d\n", pin, incoming);
			if(incoming == -1)
			{
				printf("[IO error on I2C]\n");
				break;
			}

			delay(50);
		}
	}

	return 0;
}
