#include "grove_dht_pro.h"


/**
 * constructor for the GroveDHT sensor
 * has default arguments for both parameters - look in the header
 * _module_type is either GroveDHT::BLUE_MODULE or GroveDHT::WHITE_MODULE
 * _pin is any digital port found on the GrovePi
 */
GrovePi::DHT::DHT(const uint8_t _module_type, const uint8_t _pin)
{
	module_type = _module_type;
	pin = _pin;
}

/**
 * function for connecting to the GrovePi
 * doesn't matter whether you call it multiple times
 * just check with the isConnected() function to see if you got a connection
 */
void GrovePi::DHT::init()
{
	initGrovePi();
}

/**
 * returns via parameters the temp and humidity
 * if there are readings error it raises an exception
 * @param temp     in Celsius degrees
 * @param humidity as a percentage between 0% to 100%
 */
void GrovePi::DHT::getReadings(float &temp, float &humidity)
{
	writeBlock(DHT_TEMP_CMD, pin, module_type);
	readByte();

	delay(50);

	uint8_t data_block[33];
	readBlock(data_block);

	for(int i = 0; i < 10; i++)
		printf("%d ", data_block[i]);
	printf("\n");

	temp = DHT::fourBytesToFloat(data_block + 1);
	humidity = DHT::fourBytesToFloat(data_block + 5);

	if(temp != temp || humidity != humidity)
		throw std::runtime_error("[GroveDHT NaN readings - check analog port]\n");

	if(!(temp > -100.0 && temp < 150.0 && humidity >= 0.0 && humidity <= 100.0))
		throw std::runtime_error("[GroveDHT bad readings - check analog port]\n");
}

/**
 * function for converting 4 unsigned bytes of data
 * into a single float
 * @param  byte_data array to hold the 4 data sets
 * @return           the float converted data
 */
float GrovePi::DHT::fourBytesToFloat(uint8_t *byte_data)
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
