/**
 * Class definition to interact with the Grove LCD RGB Display
 * Original code in Python - https://github.com/DexterInd/GrovePi/blob/master/Software/Python/grove_rgb_lcd/grove_rgb_lcd.py
 * 
 * I2C Definition: https://en.wikipedia.org/wiki/I%C2%B2C
 * I2C Bus Specification: http://www.nxp.com/documents/user_manual/UM10204.pdf
 * LCD Datasheet - Hitachi HD44780: https://www.sparkfun.com/datasheets/LCD/HD44780.pdf
 * 
 * 
 * @Author: Salvatore Castro
 * @Date: February 20,2017
 */

'use strict';

const sleep     = require('sleep');

const DISPLAY_RGB_ADDR  = 0x62; // 6 = 0110, 2 = 0010
const DISPLAY_TEXT_ADDR = 0x3e; // 3 = 0011, e = 1110

// Red    ==> Red = 255, Green = 0,   Blue = 0
// Yellow ==> Red = 255, Green = 255, Blue = 0
// Blue   ==> Red = 55,  Green = 55,  Blue = 255
const colorRed    = [255,  0,  0];
const colorYellow = [255,255,  0];
const colorBlue   = [ 55, 55,255];
const colorBlack  = [  0,  0,  0];
const colorPink   = [238,  0,238];

var i2c = null;

/**
 * Constructor 
 * @param i2c1	I2C Comm port display is connected on
 */
var GroveLCDRGBDisplay = class GroveLCDRGBDisplay {
	constructor(i2c) { 
//		console.log("constructor");
		this.i2c = i2c;
//		console.log("I2C 1 - Set: "+this.i2c);
		this.i2c.writeByteSync(DISPLAY_RGB_ADDR,0,0); // Backlight Initialization
		this.i2c.writeByteSync(DISPLAY_RGB_ADDR,1,0); // Disable cursor blinking (ie Blinky mode)

		// https://www.sparkfun.com/datasheets/LCD/HD44780.pdf on page #23 on Instruction Register
		// when the address counter is 08H, the cursor position is displayed at DDRAM address 0x08.
		// 
		// Flags for function set derrived from C code here: https://github.com/Seeed-Studio/Grove_LCD_RGB_Backlight/blob/master/rgb_lcd.h and rgb_lcd.cpp
		// Flags are all set but I can't find documentation on this 
		// +------------------ 0x8_ (1___) - ?
		// |+----------------- 0x4_ (_1__) - ?
		// ||+---------------- 0x2_ (__1_) - ?
		// |||+--------------- 0x1_ (___1) - ?
		// ||||
		// |||| +------------- 0x08 (1___) - ?
		// |||| |+------------ 0x04 (_1__) - ?
		// |||| ||+----------- 0x02 (__1_) - ?
		// |||| |||+---------- 0x01 (___1) - ?
		// 1111 1111 == 0xff
		// Data flags set here are 0xff in .cpp and 0xaa in python
		// REG_OUTPUT == 0x08 
		// REG_OUTPUT -> Set LEDs controllable by both PWM and GRPPWM registers 
		//this.i2c.writeByteSync(DISPLAY_RGB_ADDR,0x08,0xaa); // To Character Generator (CG) Addr -> LCD_DISPLAYCONTROL 0x08, 0xaa = 1010 1010 ==> Original in Python
		this.i2c.writeByteSync(DISPLAY_RGB_ADDR,0x08,0xff); // I can't find documentation on this...in the referenced .cpp; differs from python but doesn't appear to impact the display
	}

	/**
	 * Usefull for callback commands that you just want to print out completed
	 *
	 *	@param	input	The string to echo out to the console display
	 */
	echo(input) {
		console.log("Echo: "+input);
		return input;
	}

	/**
	 * Commands send to the LCD display to control the color
	 * 
	 * @param r	Red
	 * @param g	Green
	 * @param b	Blue
	 */
	setRGB(r, g, b) {
//		this.i2c.writeByteSync(DISPLAY_RGB_ADDR,0x08,0xff); // To Character Generator (CG) Addr 0x62 -> LCD_DISPLAYCONTROL 0x08, 0xaa = 1010 1010
		this.i2c.writeByteSync(DISPLAY_RGB_ADDR,4,r);
		this.i2c.writeByteSync(DISPLAY_RGB_ADDR,3,g);
		this.i2c.writeByteSync(DISPLAY_RGB_ADDR,2,b);
	}

	setRGBAry(rgb) {
		//console.log("setRGB: "+rgb);
		this.i2c.writeByteSync(DISPLAY_RGB_ADDR,4,rgb[0]);
		this.i2c.writeByteSync(DISPLAY_RGB_ADDR,3,rgb[1]);
		this.i2c.writeByteSync(DISPLAY_RGB_ADDR,2,rgb[2]);
	}

	/**
	 * Command that is sent as a Byte to the command register of the LCD display
	 * 
	 * @param cmd	Command sent to the LCD
	 */
	textCommand(cmd) {
		// Every now and then the synch write fails with an I/O Bus error...need to wait and then retry
		try {
			this.i2c.writeByteSync(DISPLAY_TEXT_ADDR, 0x80, cmd); // To Text -> LCD SET Display Data RAM ADDR 0x80 -> command byte
		} catch (err) {
			sleep.msleep(5);
			this.i2c.writeByteSync(DISPLAY_TEXT_ADDR, 0x80, cmd); // To Text -> LCD SET Display Data RAM ADDR 0x80 -> command byte
			console.log("GroveLCDRGBDisplay.setText.textCommand exception caught: "+err);
		}
	}

	/**
	 * Requires - https://www.npmjs.com/package/sleep 
	 * LCD Datasheet - https://github.com/SeeedDocument/Grove_LCD_RGB_Backlight/blob/master/Grove-LCD_RGB_Backlight.md
	 * 
	 * sleep  - seconds
	 * msleep - milliseconds
	 * usleep - microseconds
	 * 
	 * @param text	Text that displays on the LCD panel
	 */
	setText(text) {
		this.textCommand(0x01); // clear display - LCD_CLEARDISPLAY 0x01s
		sleep.msleep(5);
		this.textCommand(0x08 | 0x04); // Display Control (LCD_DISPLAYCONTROL 8 = 1000) ==> LCD_MOVERIGHT Entry Mode (LCD_ENTRYMODESET 4 = 0100)...could just use 0x0c (c=1100)
		this.textCommand(0x20 | 0x08); // Function set (LCD_FUNCTIONSET 2 = 0010)  ==>   LCD_2LINE Display Control (LCD_DISPLAYCONTROL 8 = 1000)...could just use 0x28
		sleep.msleep(5);
		var count = 0;
		var row = 0;
		for (var i = 0, len = text.length; i < len; i++) {
			if (text[i] === '\n' || count === 16) {
				count = 0;
				row++;
				if (row === 2)
					break;
				// See page #12 in HD44780.pdf for documentation on this for the 2-line display
				this.textCommand(0xc0) // Move cursor to the next line --- col = (row == 0 ? col|0x80 : col|0xc0); unsigned char dta[2] = {0x80, col}; 8 (1000),  c (1100)
				if (text[i] === '\n')
					continue;
			}
			count++;
			// Every now and then the synch write fails with an I/O Bus error...need to wait and then retry
			try {
				this.i2c.writeByteSync(DISPLAY_TEXT_ADDR, 0x40, text[i].charCodeAt(0)); // LCD SET Character Generator ADDR 0x40 -> Character Byte
			} catch (err) {
				sleep.msleep(5);
				this.i2c.writeByteSync(DISPLAY_TEXT_ADDR, 0x40, text[i].charCodeAt(0)); // LCD SET Character Generator ADDR 0x40 -> Character Byte
				console.log("GroveLCDRGBDisplay.setText.setText exception caught: "+err);
			}
		}
	}

	/**
	 *  Reset the display to only show the display message; useful on exit of program
	 */
	resetDisplay(displayMsg) {
		this.setText(displayMsg);
		this.setRGBAry(colorBlue);
	}

	/**
	 *  Reset the display to only show the display message; useful on exit of program
	 */
	turnOffDisplay() {
		this.textCommand(0x01); // clear display - LCD_CLEARDISPLAY 0x01s
		//sleep.msleep(50);
		this.setRGBAry(colorBlack);
	}	
}

module.exports = GroveLCDRGBDisplay;
