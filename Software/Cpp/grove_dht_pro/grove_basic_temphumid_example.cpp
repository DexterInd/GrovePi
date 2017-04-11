//
// GrovePi Example for using the Grove Temperature & Humidity Sensor Pro
// (http://www.seeedstudio.com/wiki/Grove_-_Temperature_and_Humidity_Sensor_Pro)
//
// The GrovePi connects the Raspberry Pi and Grove sensors.
// You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
//
// Have a question about this example?  Ask on the forums here:  http://forum.dexterindustries.com/c/grovepi
//
/*
## License

   The MIT License (MIT)

   GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
   Copyright (C) 2017  Dexter Industries

   Permission is hereby granted, free of charge, to any person obtaining a copy
   of this software and associated documentation files (the "Software"), to deal
   in the Software without restriction, including without limitation the rights
   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
   copies of the Software, and to permit persons to whom the Software is
   furnished to do so, subject to the following conditions:

   The above copyright notice and this permission notice shall be included in
   all copies or substantial portions of the Software.

   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
   THE SOFTWARE.
*/

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
