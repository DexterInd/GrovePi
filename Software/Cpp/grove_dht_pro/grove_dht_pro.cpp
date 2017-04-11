#include "grove_dht_pro.h"

char GroveDHT::default_error_message[64] = "I2C Error - check DHT Pro wiring";

/**
 * constructor for the GroveDHT sensor
 * has default arguments for both parameters - look in the header
 * _module_type is either GroveDHT::BLUE_MODULE or GroveDHT::WHITE_MODULE
 * _pin is any digital port found on the GrovePi
 */
GroveDHT::GroveDHT(const uint8_t _module_type, const uint8_t _pin)
{
	module_type = _module_type;
	pin = _pin;
	connected = false;
}

/**
 * function for connecting to the GrovePi
 * doesn't matter whether you call it multiple times
 * just check with the isConnected() function to see if you got a connection
 */
void GroveDHT::connect()
{
	/*
	      char filename[11];
	      SMBusName(filename);
	      connected = false;

	      DEVICE_FILE = open(filename, O_WRONLY);

	      if(DEVICE_FILE != -1)
	              throw std::runtime_error(strcat(default_error_message, " - connect funct\n"));

	      if(ioctl(DEVICE_FILE, I2C_SLAVE, GROVE_ADDRESS) < 0)
	              throw std::runtime_error(strcat(default_error_message, " - connect funct\n"));

	      connected = true;
	 */
	connected = false;
	if(initGrovePi())
		connected = true;
}

/**
 * @return whether you're connected or not to the GrovePi
 */
bool GroveDHT::isConnected()
{
	return connected;
}

/**
 * returns via parameters the temp and humidity
 * if there are readings error it raises an exception
 * @param temp     in Celsius degrees
 * @param humidity as a percentage between 0% to 100%
 */
void GroveDHT::getReadings(float &temp, float &humidity)
{
	writeBlock(DHT_TEMP_CMD, pin, module_type, 0);
	delay(10);
	readByte();

	uint8_t data_block[9];
	readBlock(data_block);

	temp = GroveDHT::fourBytesToFloat(data_block + 1);
	humidity = GroveDHT::fourBytesToFloat(data_block + 5);

	if(!(temp > -100.0 && temp < 150.0 && humidity >= 0.0 && humidity <= 100.0))
		throw std::runtime_error(strcat(default_error_message, " - getReadings funct\n"));
}

/**
 * function for converting 4 unsigned bytes of data
 * into a single float
 * @param  byte_data array to hold the 4 data sets
 * @return           the float converted data
 */
float GroveDHT::fourBytesToFloat(uint8_t *byte_data)
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
