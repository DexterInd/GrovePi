// GrovePi C++ library
// v0.2
//
// This library provides the basic functions for using the GrovePi in C
//
// The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
//
// Have a question about this example?  Ask on the forums here: http://forum.dexterindustries.com/c/grovepi
//
//      History
//      ------------------------------------------------
//      Author		Date                    Comments
//	    Karan		  28 Dec 2015		            Initial Authoring
//	    Robert		April 2017							  Continuing

/*
   License

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

static const bool DEBUG = false;
static const int RBUFFER_SIZE = 32;
static const int WBUFFER_SIZE = 5;

static int file_device = 0;

static const uint8_t DIGITAL_READ = 1;
static const uint8_t DIGITAL_WRITE = 2;
static const uint8_t ANALOG_READ = 3;
static const uint8_t ANALOG_WRITE = 4;
static const uint8_t PIN_MODE = 5;
static const uint8_t USONIC_READ = 7;

const uint8_t INPUT = 0;
const uint8_t OUTPUT = 1;
const bool LOW = false;
const bool HIGH = true;
uint8_t GROVE_ADDRESS = 0x04;

/**
 * determines the revision of the raspberry hardware
 * @return revision number
 */
static uint8_t gpioHardwareRevision()
{
	int revision = 0;
	FILE * filp = fopen("/proc/cpuinfo", "r");
	char buffer[512];
	char term;

	if(filp != NULL)
	{
		while(fgets(buffer,sizeof(buffer),filp) != NULL)
		{
			if(!strncasecmp("revision\t", buffer, 9))
			{
				if(sscanf(buffer + strlen(buffer) - 5, "%x%c", &revision, &term) == 2)
				{
					if(term == '\n')
						break;
					revision = 0;
				}
			}
		}
		fclose(filp);
	}
	return revision;
}

/**
 * determines wheter I2C is found at "/dev/i2c-0" or "/dev/i2c-1"
 * depending on the raspberry model
 *
 * @param smbus_name string to hold the filename
 *
 * hw_rev    0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15
 * Type.1    X  X  -  -  X  -  -  X  X  X  X  X  -  -  X  X
 * Type.2    -  -  X  X  X  -  -  X  X  X  X  X  -  -  X  X
 * Type.3          X  X  X  X  X  X  X  X  X  X  X  X  X  X
 *
 * hw_rev    16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31
 * Type.1    -  X  X  -  -  X  X  X  X  X  -  -  -  -  -  -
 * Type.2    -  X  X  -  -  -  X  X  X  X  -  X  X  X  X  X
 * Type.3    X  X  X  X  X  X  X  X  X  X  X  X  -  -  -  -
 *
 */
void SMBusName(char *smbus_name)
{
	unsigned int hw_revision = gpioHardwareRevision();
	unsigned int smbus_rev;

	if(hw_revision < 4)
		// type 1
		smbus_rev = 1;
	else if(hw_revision < 16)
		// type 2
		smbus_rev = 2;
	else
		// type 3
		smbus_rev = 3;

	if(smbus_rev == 2 || smbus_rev == 3)
		strcpy(smbus_name, "/dev/i2c-1");
	else
		strcpy(smbus_name, "/dev/i2c-0");
}

/**
 * tries to get communication w/ the GrovePi
 * @param  address 7-bit address of the slave device
 * @return         true on success, otherwise false
 */
bool initGrovePi()
{
	bool success = true;
	char filename[11]; // enough to hold "/dev/i2c-x"
	SMBusName(filename);

	// open port for read/write operation
	if((file_device = open(filename, O_RDWR)) < 0)
	{
		printf("Failed to open i2c port\n");
		success = false;
	}
	// setting up port options and address of the device
	else if(ioctl(file_device, I2C_SLAVE, GROVE_ADDRESS) < 0)
	{
		printf("Unable to get bus access to talk to slave\n");
		success = false;
	}

	return success;
}

void setGrovePiAddress(uint8_t address)
{
	GROVE_ADDRESS = address;
}

/**
 * writes a block of [WBUFFER_SIZE] bytes to the slave i2c device
 * @param  command    command to send to GrovePi
 * @param  pin_number number
 * @param  opt1       optional argument depending on sensor/actuator/etc
 * @param  opt2       optional argument depending on sensor/actuator/etc
 * @return            always true
 */
bool writeBlock(uint8_t command, uint8_t pin_number, uint8_t opt1, uint8_t opt2)
{
	int debug_code;
	uint8_t data_block[5] = {0, command, pin_number, opt1, opt2};

	// puts data on the i2c line
	debug_code = i2c_smbus_write_i2c_block_data(file_device, 1, 5, &data_block[0]);
	if(DEBUG)
		printf("[write block: %s]\n", (debug_code == -1 ? "error" : "ok"));

	return true;
}

/**
 * sends a single byte to the i2c slave
 * @param  byte_val byte to be sent
 * @return          true on success, otherwise false
 */
bool writeByte(uint8_t byte_val)
{
	bool success = true;
	int data_block[WBUFFER_SIZE] = {byte_val};

	// try to send the byte to the i2c slave
	if((write(file_device, data_block, 1)) != 1)
	{
		printf("[write byte: error]\n");
		success = false;
	}

	return success;
}

/**
 * reads a block of [RBUFFER_SIZE] bytes from the slave device
 * @param  data_block pointer to hold the read data
 * @return            always true
 */
bool readBlock(uint8_t *data_block)
{
	int debug_code;
	debug_code = i2c_smbus_read_i2c_block_data(file_device, 1, RBUFFER_SIZE, data_block);

	if(DEBUG)
		printf("[read block: %s]\n", (debug_code == -1 ? "error" : "ok"));

	return true;
}

/**
 * reads 1 byte from the slave device
 * @return value read from the slave device
 */
uint8_t readByte()
{
	uint8_t value = i2c_smbus_read_byte(file_device);

	if(DEBUG)
		printf("[read byte: %s]\n", (value == 255 ? "error" : "ok"));

	return value;
}

/**
 * sleep raspberry
 * @param milliseconds time
 */
void delay(unsigned int milliseconds)
{
	usleep(milliseconds * 1000);
}

/**
 * set pin as OUTPUT or INPUT
 * @param  pin  number
 * @param  mode OUTPUT/INPUT
 * @return      always true
 */
bool pinMode(uint8_t pin, uint8_t mode)
{
	return writeBlock(PIN_MODE, pin, mode);
}

/**
 * set a pin as HIGH or LOW
 * @param  pin   number
 * @param  value HIGH or LOW
 * @return       always true
 */
bool digitalWrite(uint8_t pin, bool value)
{
	return writeBlock(DIGITAL_WRITE, pin, (uint8_t)value);
}

/**
 * reads whether a pin is HIGH or LOW
 * @param  pin number
 * @return     HIGH or LOW
 */
uint8_t digitalRead(uint8_t pin)
{
	writeBlock(DIGITAL_READ, pin);
	// wait 10 ms to receive data
	delay(10);
	return readByte();
}

/**
 * describe at a desired pin a voltage between 0 and VCC
 * @param  pin   number
 * @param  value 0-255
 * @return       always true
 */
bool analogWrite(uint8_t pin, uint8_t value)
{
	return writeBlock(ANALOG_WRITE, pin, value);
}

/**
 * reads analog data from grovepi sensor(s)
 * @param  pin number
 * @return     16-bit data
 */
int analogRead(uint8_t pin)
{
	uint8_t data[32];
	writeBlock(ANALOG_READ, pin);
	readBlock(data);

	int output = (data[1] << 8) + data[2];
	if(output == 65535)
		output = -1;
	return output;
}

/**
 * to be completed
 * @param  pin number
 * @return     time taken for the sound to travel back?
 */
int ultrasonicRead(uint8_t pin)
{
	uint8_t incoming[32];
	int output;
	writeBlock(USONIC_READ, pin);
	delay(60);

	readByte();
	readBlock(incoming);

	output = (incoming[1] << 8) + incoming[2];
	if(output == (2 << 16) - 1)
		output = -1;

	return output;
}

const char* I2CError::detailError()
{
	return this->what();
}
