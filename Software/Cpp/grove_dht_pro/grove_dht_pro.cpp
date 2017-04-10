#include "grove_dht_pro.h"

char GroveDHT::default_error_message[64] = "I2C Error - check DHT Pro wiring";

GroveDHT::GroveDHT(const uint8_t _module_type, const uint8_t _pin)
{
	module_type = _module_type;
	pin = _pin;
	connected = false;
}

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

bool GroveDHT::isConnected()
{
	return connected;
}

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

float GroveDHT::fourBytesToFloat(uint8_t *data)
{
	float output;

	*((uint8_t*)(&output) + 3) = data[3];
	*((uint8_t*)(&output) + 2) = data[2];
	*((uint8_t*)(&output) + 1) = data[1];
	*((uint8_t*)(&output) + 0) = data[0];

	return output;
}
