// GrovePi Example for using the analog read.

// GrovePi is an electronics board designed by Dexter Industries that you can connect to hundreds of 
// different sensors, so you can program them to monitor, control, and automate devices in your life.  
// See more about the GrovePi here:  http://www.dexterindustries.com/grovepi/

#include "grovepi.h"

int main(void)
{		
	int adata;
	
	//Exit on failure to start communications with the GrovePi
	if(init()==-1)
		exit(1);
	
	while(1)
	{
		adata=analogRead(0);
		printf("analog read %d\n",adata);
		if(adata==-1)
			printf("IO Error");
	}
   	return 1;
}
