#include "grovepi.h"
#include "grove_dht_pro.h"

int main()
{
	int sensorPin = 4;
	int max_retries = 5;
	int current_retries = 0;
	GroveDHT dht(GroveDHT::BLUE_MODULE, sensorPin);
	float temp, humidity;

	while(!dht.isConnected())
	{
		dht.connect();
		delay(10);
	}

	while(current_retries < max_retries)
	{
		try
		{
			dht.getReadings(temp, humidity);
			printf("[temp = %.02f C][humidity = %.02f%%]\n", temp, humidity);
		}
		catch (I2CError &error)
		{
			if(current_retries < max_retries)
				current_retries += 1;
			else
				printf(error.detailError());
		}
		delay(100);
	}

	return 0;
}
