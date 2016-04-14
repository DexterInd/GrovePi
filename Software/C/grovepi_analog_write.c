// GrovePi Example for using the analog write 

// GrovePi is an electronics board designed by Dexter Industries that you can connect to hundreds of 
// different sensors, so you can program them to monitor, control, and automate devices in your life.  
// See more about the GrovePi here:  http://www.dexterindustries.com/grovepi/


#include "grovepi.h"
//gcc grovepi_analog_write.c grovepi.c -Wall
int main(void)
{		
	int i;
	
	//Exit on failure to start communications with the GrovePi
	if(init()==-1)
		exit(1);
	
	while(1)
	{
		for(i=0;i<256;i++)
		{
			printf("%d\n", i);
			//Write the PWM value
			analogWrite(3,i);
			//Sleep for 10ms
			pi_sleep(10);
		}
	}
   	return 1;
}
