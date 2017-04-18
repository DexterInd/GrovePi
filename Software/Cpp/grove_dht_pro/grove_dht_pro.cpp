#include "grove_dht_pro.h"

using std::runtime_error;
using GrovePi::DHT;

/**
 * function for connecting to the GrovePi
 * doesn't matter whether you call it multiple times
 * just check with the isConnected() function to see if you got a connection
 */
void DHT::init()
{
	initGrovePi();
}

/**
 * returns via its parameters the temperature and humidity
 * this function is NaN-proof
 * it always gives "accepted" values
 *
 * if bad values are read, then it will retry reading them
 * and check if they are okay for a number of [MAX_RETRIES] times
 * before throwing a [runtime_error] exception
 *
 * @param temp     in Celsius degrees
 * @param humidity in percentage values
 */
void DHT::getSafeData(float &temp, float &humidity)
{
	int current_retry  = 0;
	this->getUnsafeData(temp, humidity); // read data from GrovePi once

	// while values got are not okay / accepteed
	while((isnan(temp) || isnan(humidity) || !this->areGoodReadings(temp, humidity))
	      && current_retry < this->MAX_RETRIES)
	{
		// reread them again
		current_retry += 1;
		this->getUnsafeData(temp, humidity);
	}

	// if even after [MAX_RETRIES] attempts at getting good values
	// nothing good came, then throw one of the bottom exceptions

	if(isnan(temp) || isnan(humidity))
		throw runtime_error("[GroveDHT NaN readings - check analog port]\n");

	if(!DHT::areGoodReadings(temp, humidity))
		throw runtime_error("[GroveDHT bad readings - check analog port]\n");
}

/**
 * function for returning via its arguments the temperature & humidity
 * it's not recommended to use this function since it might throw
 * some NaN or out-of-interval values
 *
 * use it if you come with your own implementation
 * or if you need it for some debugging
 *
 * @param temp     in Celsius degrees
 * @param humidity in percentage values
 */
void DHT::getUnsafeData(float &temp, float &humidity)
{
	writeBlock(this->DHT_TEMP_CMD, this->pin, this->module_type);
	readByte();

	uint8_t data_block[33];
	readBlock(data_block);

	temp = DHT::fourBytesToFloat(data_block + 1);
	humidity = DHT::fourBytesToFloat(data_block + 5);
}

/**
 * function for converting 4 unsigned bytes of data
 * into a single float
 * @param  byte_data array to hold the 4 data sets
 * @return           the float converted data
 */
const float DHT::fourBytesToFloat(uint8_t *byte_data)
{
	float output;

	// reinterpret_cast guarantees that if you cast a pointer
	// to a different type, and then reinterpret_cast it back
	// to the original type, you get the original value.
	//
	// as opposed to the static_cast where it only guarantees
	// the address is preserved
	//
	// so we take the 1st address &byte_data[0],
	// the 5th address &byte_data[4] (the end address)
	// and translate the output into a unsigned byte type
	std::copy(reinterpret_cast<const uint8_t*>(&byte_data[0]),
	          reinterpret_cast<const uint8_t*>(&byte_data[4]),
	          reinterpret_cast<uint8_t*>(&output));

	return output;
}

const bool DHT::areGoodReadings(int temp, int humidity)
{
	return (temp > -100.0 && temp < 150.0 && humidity >= 0.0 && humidity <= 100.0);
}
