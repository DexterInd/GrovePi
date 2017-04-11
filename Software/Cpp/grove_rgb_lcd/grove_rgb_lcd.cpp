#include "grove_rgb_lcd.h"

uint8_t GroveLCD::DISPLAY_RGB_ADDR = 0x62;
uint8_t GroveLCD::DISPLAY_TEXT_ADDR = 0x3e;

uint8_t GroveLCD::CLEAR_DISPLAY = 0x01;
uint8_t GroveLCD::DISPLAY_ON = 0x08;
uint8_t GroveLCD::NO_CURSOR = 0x04;
uint8_t GroveLCD::ENABLE_2ROWS = 0x28;
uint8_t GroveLCD::PROGRAM_MODE = 0x80;
uint8_t GroveLCD::NEW_ROW = 0xc0;
uint8_t GroveLCD::DISPLAY_CHAR = 0x40;
char GroveLCD::default_error_message[64] = "I2C Error - check LCD wiring";

GroveLCD::GroveLCD()
{
	connected = false;
}

void GroveLCD::connect()
{
	char filename[11];
	SMBusName(filename);

	DEVICE_FILE = open(filename, O_WRONLY);

	if(DEVICE_FILE != -1)
	{
		connected = false;
		throw std::runtime_error(strcat(default_error_message, " - connect funct\n"));
	}

	connected = true;
}

bool GroveLCD::isConnected()
{
	return connected;
}

/**
 * set rgb color
 * if there are writes errors, then it throws exception
 * @param red   8-bit
 * @param green 8-bit
 * @param blue  8-bit
 */
void GroveLCD::setRGB(uint8_t red, uint8_t green, uint8_t blue)
{
	selectSlave(DISPLAY_RGB_ADDR);

	int error_sum = 0;
	error_sum += i2c_smbus_write_byte_data(DEVICE_FILE, 0x00, 0x00);
	error_sum += i2c_smbus_write_byte_data(DEVICE_FILE, 0x01, 0x00);
	error_sum += i2c_smbus_write_byte_data(DEVICE_FILE, 0x08, 0xaa);
	error_sum += i2c_smbus_write_byte_data(DEVICE_FILE, 0x04, red);
	error_sum += i2c_smbus_write_byte_data(DEVICE_FILE, 0x03, green);
	error_sum += i2c_smbus_write_byte_data(DEVICE_FILE, 0x02, blue);

	if(error_sum < 0)
		throw std::runtime_error(strcat(default_error_message, " - setRGB funct\n"));
}

/**
 *  Grove RGB LCD
 *
 *     |                  Column
 * ------------------------------------------------------
 * Row | 1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16
 * ------------------------------------------------------
 * 1   | x  x  x  x  x  x  x  x  x  x  x  x  x  x  x  x
 * 2   | x  x  x  x  x  x  x  x  x  x  x  x  x  x  x  x
 * ------------------------------------------------------
 *
 * Whatever text is sent to the LCD via the [str] variable
 * Gets printed on the screen.
 * The limit of text is determined by the amount of available
 * Characters on the LCD screen.
 *
 * Every newline char ['\n'] takes the cursor onto the next line
 * (aka on the row no. 2) and uses that space
 * This means that if we have a text such "Hello\n World!",
 * The first 5 characters of the word "Hello" get printed on the first line,
 * whilst the rest of the string gets printed onto the 2nd line.
 * So, if you use the newline char ['\n'] before the row ends,
 * You will end up with less space to put the rest of the characters (aka the last line)
 *
 * If the text your putting occupies more than the LCD is capable of showing,
 * Than the LCD will display only the first 16x2 characters.
 *
 * @param string of maximum 32 characters excluding the NULL character.
 */
void GroveLCD::setText(const char *str)
{
	selectSlave(DISPLAY_TEXT_ADDR);

	sendCommand(CLEAR_DISPLAY);
	delay(50);
	sendCommand(DISPLAY_ON | NO_CURSOR);
	sendCommand(ENABLE_2ROWS);
	delay(50);

	int length = strlen(str);
	uint8_t row = 0;
	int error;
	for(int i = 0; i <= length; i++)
	{
		if(i % 15 == 0 || str[i] == '\n')
		{
			row += 1;
			if(row == 2)
				break;

			sendCommand(NEW_ROW);
			if(str[i] == '\n')
				continue;
		}
		error = i2c_smbus_write_byte_data(DISPLAY_CHAR, DISPLAY_CHAR, uint8_t(str[i]));
		if(error < 0)
			throw std::runtime_error(strcat(default_error_message, " - setText funct\n"));
	}
}

void GroveLCD::sendCommand(uint8_t command)
{
	int error = i2c_smbus_write_byte_data(DISPLAY_CHAR, PROGRAM_MODE, command);

	if(error < 0)
		throw std::runtime_error(strcat(default_error_message, " - sendCommand funct\n"));
}

/**
 * the LCD has 2 slaves
 * 1 for the RGB backlight color
 * 1 for the actual text
 * therefore there are 2 adresses
 * @param slave 7-bit address
 */
void GroveLCD::selectSlave(uint8_t slave)
{
	int error = ioctl(DEVICE_FILE, I2C_SLAVE, slave);
	if(error < 0)
		throw std::runtime_error(strcat(default_error_message, " - selectSlave funct\n"));
}