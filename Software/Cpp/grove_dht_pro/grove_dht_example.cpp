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

using GrovePi::DHT;
using GrovePi::delay;
using GrovePi::I2CError;

// sudo g++ -Wall grovepi.cpp grove_dht_pro.cpp grove_dht_example.cpp -o grove_dht_example.out -> without grovepicpp package installed
// sudo g++ -Wall -lgrovepicpp grove_dht_pro.cpp grove_dht_example.cpp -o grove_dht_example.out -> with grovepicpp package installed

int main()
{
	int sensorPin = 4; // digital port (D4) to which we have DTH serial sensor connected
	float temp = 0, humidity = 0; // variables to hold data from the DHT sensor

	// initialize the BLUE module (got from the GrovePi kit)
	// and use digital port 4 for the DHT sensor
	DHT dht = DHT(DHT::BLUE_MODULE, sensorPin);

	try
	{
		dht.init(); // same as initGrovePi

		// do this indefinitely
		while(true)
		{
			// read the DHT sensor values
			dht.getSafeData(temp, humidity);

			// and print them on the screen
			printf("[temp = %.02f C][humidity = %.02f%%]\n", temp, humidity);

			// and wait 100 before the other reading
			// so we don't overflow the terminal
			delay(100);
		}
	}
	catch(I2CError &error)
	{
		// I2C error while reading / writing
		printf(error.detail());
		return -1;
	}
	catch(std::runtime_error &e)
	{
		// catch error on number values
		// NaN & bad value readings
		printf(e.what());
		return -2;
	}

	return 0;
}
