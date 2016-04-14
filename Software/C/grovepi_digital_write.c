//GrovePi Example for using the digital write command
#include "grovepi.h"
//gcc grovepi_digital_write.c grovepi.c -Wall
//
//
// GrovePi is an electronics board designed by Dexter Industries that you can connect to hundreds of 
// different sensors, so you can program them to monitor, control, and automate devices in your life.  
// See more about the GrovePi here:  http://www.dexterindustries.com/grovepi/
//
int main(void)
{		
	//Exit on failure to start communications with the GrovePi
	if(init()==-1)
		exit(1);
	
	//Set pin mode to output
	pinMode(4,1);
	while(1)
	{
		digitalWrite(4,1);
		pi_sleep(500);
		digitalWrite(4,0);
		pi_sleep(500);
	}
   	return 1;
}
