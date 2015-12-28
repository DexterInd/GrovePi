//GrovePi Example for using the digital write command
#include "grovepi.h"
//gcc grovepi_digital_write.c grovepi.c -Wall
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
