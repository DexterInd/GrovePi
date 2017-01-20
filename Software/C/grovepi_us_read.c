#include "grovepi.h"

int main(void)
{		
	int adata;
	
	//Exit on failure to start communications with the GrovePi
	if(init()==-1)
		exit(1);
	
	while(1)
	{
		adata=ultrasonicRead(4);
		printf("ultasonic read %d\n",adata);
		if(adata==-1)
			printf("IO Error");
	}
   	return 1;
}
