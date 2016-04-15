// GrovePi Example for using the digital read command
// http://dexterindustries.com/grovepi

// GrovePi is an electronics board designed by Dexter Industries that you can connect to hundreds of 
// different sensors, so you can program them to monitor, control, and automate devices in your life.  
// See more about the GrovePi here:  http://www.dexterindustries.com/grovepi/

#include "grovepi.h"
//gcc grovepi_digital_read.c grovepi.c -Wall
int main(void)
{		
	int dval;
	
	//Exit on failure to start communications with the GrovePi
	if(init()==-1)
		exit(1);
	
	//Set pin mode to input
	pinMode(4,0);
	while(1)
	{
		dval=digitalRead(2);
		printf("Digital read %d\n", dval);
		//Sleep for 50ms
		pi_sleep(50);
	}
   	return 1;
}
