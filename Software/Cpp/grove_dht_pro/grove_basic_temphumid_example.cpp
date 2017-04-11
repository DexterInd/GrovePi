#include "grovepi.h"
#include "grove_dht_pro.h"

int main()
{
	int sensorPin = 4; // digital port to which we have DTH sensor connected
	int max_retries = 5; // maximum number of consecutive I2C errors allowed
	int current_retries = 0; // current number of errors encountered

	// initialize the BLUE module (got from the GrovePi kit)
	// and use digital port 4 for the DHT sensor
	GroveDHT dht(GroveDHT::BLUE_MODULE, sensorPin);

	float temp, humidity; // variables to hold data from the DHT sensor

	// while we haven't got a connection with the GrovePi
	while(!dht.isConnected())
	{
		dht.connect(); // try to connect
		delay(10); // and wait 10 ms on each turn
	}

	// while number of errors stays below the threshold
	while(current_retries < max_retries)
	{
		// do this
		try
		{
			// reset the counter since we care
			// about the consecutives
			current_retries = 0;
			// read the DHT sensor values
			dht.getReadings(temp, humidity);
			// and print them on the screen
			printf("[temp = %.02f C][humidity = %.02f%%]\n", temp, humidity);
		}
		catch (I2CError &error) // if an I2C error occurred
		{
			// check if the threshold is reached
			if(current_retries < max_retries)
				current_retries += 1;
			else
				// if threshold has been reached
				// then print the error
				// and exit the program
				printf(error.detailError());
		}
		delay(100);
	}

	return 0;
}
