/*
Bitbanged the GPIO to simulate SPI interface.
Used CLKPIN and DATPIN.
LED1,2,3 gives the indicator of different light levels.

Since P9813 and PN532 are using SPI, but P9813 is without ChipSelect wire, so any data on MOSI would be accepted by P9813, that leads to blinking light sometimes.

But this simulation is also unstable when raspberry pi under high load.

Reference here: http://www.seeedstudio.com/wiki/File:P9813_datasheet.pdf

Verified for 1 LED, and this should be compatible with multiple LEDs. It is said that 1024 LEDs is allowed.

This project is created by @DaochenShi (shidaochen@live.com)
*/


#include <wiringPi.h>	// GPIO handling

// use wiringPi pinout
#define CLKPIN 16
#define DATPIN 15

// 20 microseconds to sleep
#define CLOCKINTERVAL 20


// This is to let other LEDs (pure light) controlled by GPIO(on/off)
// Comment out the line would control P9813 only.
//#define GPIO_PURE_LED

#ifdef GPIO_PURE_LED
	// use wiringPi pinout
	#define GPIO_PURE_LED1	0
	#define GPIO_PURE_LED2	2
	#define GPIO_PURE_LED3	3
#endif

// Send a byte bit by bit using digitalWrite
void sendByte(unsigned char b);

// Send a color(RGB) information to LED.
void sendColor(unsigned char r, unsigned char g, unsigned char b);

// Set the color, used stored previous RGB information to avoid writing the same thing repeatedly.
// This is 'buffered'. If the color is the same as previous color, we might ignore it.
// Advantage: Fewer GPIO write leads to less CPU costs.
// Disadvantage: Your request may not be applied, apply once every 2^8 times.
void setColorRGBbuffered(unsigned char r, unsigned char g, unsigned char b);

// Set the color to LED, or the first LED.
// This is not 'buffered', every time you invoke this method, it would send the signals directly to the bus.
// Advantage: What you see is what you want.
// Disadvantage: If you invoke this all the time, and write the same color, it costs a lot of CPU.
void setColorRGB(unsigned char r, unsigned char g, unsigned char b);

// Set the color with multiple LEDs.
// Not tested yet.
void setColorRGBs(unsigned char* r, unsigned char* g, unsigned char* b, int count);

// Initializing
// I noted this because occasionally the light was brought up, and cannot be set.
// Because I rebooted the Pi, and forgot to set to OUTPUT direction.
void initialP9813GPIO();