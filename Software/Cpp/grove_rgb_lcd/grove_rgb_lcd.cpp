#include "grove_rgb_lcd.h"

using GrovePi::LCD;

uint8_t LCD::DISPLAY_RGB_ADDR = 0x62;
uint8_t LCD::DISPLAY_TEXT_ADDR = 0x3e;

uint8_t LCD::CLEAR_DISPLAY = 0x01;
uint8_t LCD::DISPLAY_ON = 0x08;
uint8_t LCD::NO_CURSOR = 0x04;
uint8_t LCD::ENABLE_2ROWS = 0x28;
uint8_t LCD::PROGRAM_MODE = 0x80;
uint8_t LCD::NEW_ROW = 0xc0;
uint8_t LCD::DISPLAY_CHAR = 0x40;
uint8_t LCD::MAX_NO_CHARS = 32;

void LCD::connect()
{
	// initializing with a random address
	// it's just important to get the device file
	this->DEVICE_FILE = initDevice(LCD::DISPLAY_TEXT_ADDR);
}

/**
 * set rgb color
 * if there are writes errors, then it throws exception
 * @param red   8-bit
 * @param green 8-bit
 * @param blue  8-bit
 */
void LCD::setRGB(uint8_t red, uint8_t green, uint8_t blue)
{
	this->selectSlave(LCD::DISPLAY_RGB_ADDR);

	this->sendCommand(0x00, 0x00);
	this->sendCommand(0x01, 0x00);
	this->sendCommand(0x08, 0xaa);
	this->sendCommand(0x04, red);
	this->sendCommand(0x03, green);
	this->sendCommand(0x02, blue);
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
void LCD::setText(const char *str)
{
	this->selectSlave(LCD::DISPLAY_TEXT_ADDR);

	this->sendCommand(LCD::PROGRAM_MODE, LCD::CLEAR_DISPLAY);
	delay(50);
	this->sendCommand(LCD::PROGRAM_MODE, LCD::DISPLAY_ON | LCD::NO_CURSOR);
	this->sendCommand(LCD::PROGRAM_MODE, LCD::ENABLE_2ROWS);
	delay(50);

	int length = strlen(str);
	bool already_had_newline = false;
	for(int i = 0; i < length && i < LCD::MAX_NO_CHARS; i++)
	{
		if(i == 16 || str[i] == '\n')
		{
			if(!already_had_newline)
			{
				already_had_newline = true;
				this->sendCommand(LCD::PROGRAM_MODE, LCD::NEW_ROW);
				if(str[i] == '\n')
					continue;
			}
			else if(str[i] == '\n')
				break;
		}

		this->sendCommand(LCD::DISPLAY_CHAR, uint8_t(str[i]));
	}
}

/**
 * function for sending data to GrovePi RGB LCD
 * @param mode    see the constants defined up top
 * @param command see the constants defined up top
 */
void LCD::sendCommand(uint8_t mode, uint8_t command)
{
	int error = i2c_smbus_write_byte_data(this->DEVICE_FILE, mode, command);

	if(error == -1)
		throw I2CError("[I2CError writing data: check LCD wirings]\n");
}

/**
 * the LCD has 2 slaves
 * 1 for the RGB backlight color
 * 1 for the actual text
 * therefore there are 2 adresses
 * @param slave 7-bit address
 */
void LCD::selectSlave(uint8_t slave)
{
	int error = ioctl(this->DEVICE_FILE, I2C_SLAVE, slave);
	if(error == -1)
		throw I2CError("[I2CError selecting LCD address]\n");
}
