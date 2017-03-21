/**
 * Class definition to interact with the Grove LCD RGB Display
 * Original code in Python - https://github.com/DexterInd/GrovePi/blob/master/Software/Python/grove_rgb_lcd/grove_rgb_lcd.py
 * 
 * I2C Definition - https://en.wikipedia.org/wiki/I%C2%B2C
 *
 * ARBITRATION ON I2C - 
 * Although conceptually a single-master bus, a slave device that supports the "host notify protocol" acts as a master to perform the notification. 
 * It seizes the bus and writes a 3-byte message to the reserved "SMBus Host" address (0x08), passing its address and two bytes of data. When two 
 * slaves try to notify the host at the same time, one of them will lose arbitration and need to retry.  
 * 
 * An alternative slave notification system uses the separate SMBALERT# signal to request attention. In this case, the host performs a 1-byte read 
 * from the reserved "SMBus Alert Response Address" (0x0c), which is a kind of broadcast address. All alerting slaves respond with a data bytes 
 * containing their own address. When the slave successfully transmits its own address (winning arbitration against others) it stops raising that interrupt. 
 * In both this and the preceding case, arbitration ensures that one slave's message will be received, and the others will know they must retry.
 * 
 * There seems to be an issue if you change the color and then set text with the I2C bus synchronous writes.  Modified to 
 * change the code to write text first and then set the display color.
 * 
 * @Author: Salvatore Castro
 * @Date: February 20,2017
 */

'use strict';

const sleep     = require('sleep');

const DISPLAY_RGB_ADDR  = 0x62;
const DISPLAY_TEXT_ADDR = 0x3e;

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
	}
	
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
		//sleep.msleep(50);
		this.i2c.writeByteSync(DISPLAY_RGB_ADDR,0,0);
		this.i2c.writeByteSync(DISPLAY_RGB_ADDR,1,0);
		this.i2c.writeByteSync(DISPLAY_RGB_ADDR,0x08,0xaa); // The reserved "SMBus Host" address (0x08)
		this.i2c.writeByteSync(DISPLAY_RGB_ADDR,4,r);
		this.i2c.writeByteSync(DISPLAY_RGB_ADDR,3,g);
		this.i2c.writeByteSync(DISPLAY_RGB_ADDR,2,b);
	}

	setRGBAry(rgb) {
		//sleep.msleep(50);
		//console.log("setRGB: "+rgb);
		this.i2c.writeByteSync(DISPLAY_RGB_ADDR,0,0);
		this.i2c.writeByteSync(DISPLAY_RGB_ADDR,1,0);
		this.i2c.writeByteSync(DISPLAY_RGB_ADDR,0x08,0xaa); // The reserved "SMBus Host" address (0x08)
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
		this.i2c.writeByteSync(DISPLAY_TEXT_ADDR, 0x80, cmd);
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
		this.i2c.writeByteSync(DISPLAY_TEXT_ADDR,0,0);
		this.i2c.writeByteSync(DISPLAY_TEXT_ADDR,1,0);
		this.i2c.writeByteSync(DISPLAY_TEXT_ADDR,0x08,0xaa); // The reserved "SMBus Host" address (0x08)
		this.textCommand(0x01);        // clear display
		sleep.msleep(50);
		this.textCommand(0x08 | 0x04); // display on(8 = 1000) and no cursor(4 = 0100)...could just use 0x0c (c=1100)
		this.textCommand(0x28);
		sleep.msleep(50);
		var count = 0;
		var row = 0;
		for (var i = 0, len = text.length; i < len; i++) {
			if (text[i] === '\n' || count === 16) {
				count = 0;
				row++;
				if (row === 2)
					break;
				this.textCommand(0xc0)
				if (text[i] === '\n')
					continue;
			}
			count++;
			this.i2c.writeByteSync(DISPLAY_TEXT_ADDR, 0x40, text[i].charCodeAt(0));
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
	 *  Reset the display and turn off LED light useful on termination
	 */
	turnOffDisplay() {
		this.textCommand(0x01); // clear display
		//sleep.msleep(50);
		this.setRGBAry(colorBlack);
	}	
}

module.exports = GroveLCDRGBDisplay;
