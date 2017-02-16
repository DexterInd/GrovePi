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

#include <stdio.h>	// printf,etc.
#include <stdlib.h>	// exit
#include <signal.h>	// for Ctrl+C
//#include <unistd.h>	// usleep
#include <time.h>	// nanosleep
#include <math.h>	// abs
#include <errno.h>	// errno

#include "P9813GPIO.h"




static struct timespec TIMCLOCKINTERVAL;

// Send a byte bit by bit using digitalWrite
void sendByte(unsigned char b)
{
	char loop = 8;
	#ifndef DRYRUN
	for(loop = 0; loop < 8; loop++)
	{
		digitalWrite(CLKPIN, LOW);
		nanosleep(&TIMCLOCKINTERVAL, NULL);
		//usleep(CLOCKINTERVAL);
		// The  ic will latch a bit of data when the rising edge of the clock coming, And the data should changed after the falling edge of the clock; 
		// Copyed from P9813 datasheet
		
		if ((b & 0x80) != 0)
			digitalWrite(DATPIN, HIGH);
		else
			digitalWrite(DATPIN, LOW);
		
		digitalWrite(CLKPIN, HIGH);
		nanosleep(&TIMCLOCKINTERVAL, NULL);
		//usleep(CLOCKINTERVAL);
		
		b <<= 1;
	}
	#endif
}

// Send a color(RGB) information to LED.
void sendColor(unsigned char r, unsigned char g, unsigned char b)
{
	unsigned char prefix = 0b11000000;
	if ((b & 0x80) == 0)	prefix |= 0b00100000;
	if ((b & 0x40) == 0)	prefix |= 0b00010000;
	if ((g & 0x80) == 0)	prefix |= 0b00001000;
	if ((g & 0x40) == 0)	prefix |= 0b00000100;
	if ((r & 0x80) == 0)	prefix |= 0b00000010;
	if ((r & 0x40) == 0)	prefix |= 0b00000001;
	
	sendByte(prefix);
	sendByte(b);sendByte(g);sendByte(r);
}

#ifdef GPIO_PURE_LED
	#ifdef GPIO_PURE_LED1
		static unsigned char LED1value = 0;
	#endif
	
	#ifdef GPIO_PURE_LED2
		static unsigned char LED2value = 0;
	#endif
	
	#ifdef GPIO_PURE_LED3
		static unsigned char LED3value = 0;
	#endif
#endif
static unsigned char previousR = 0;
static unsigned char previousG = 0;
static unsigned char previousB = 0;
static unsigned char unchangedTimes = 0;

// Set the color, used stored previous RGB information to avoid writing the same thing repeatedly.
// This is 'buffered'. If the color is the same as previous color, we might ignore it.
// Also, this function handled GPIO pure LEDs, so remove GPIO_PURE_LED to get access only to P9813.
// Advantage: Fewer GPIO write leads to less CPU costs.
// Disadvantage: Your request may not be applied, apply once every 2^8 times.
void setColorRGBbuffered(unsigned char r, unsigned char g, unsigned char b)
{
	unsigned char max = 0;
	max = (max > r) ? max : r;
	max = (max > g) ? max : g;
	max = (max > b) ? max : b;

#ifdef GPIO_PURE_LED

	#ifdef GPIO_PURE_LED1
		if (LED1value != (max > 0x40))
		{
			digitalWrite(GPIO_PURE_LED1, (max > 0x40));
			LED1value = (max > 0x40);
		}
		else
		{
			unchangedTimes++;
		#ifdef P9813DEBUG
			printf("Unchanged this time, %d\n", unchangedTimes);
		#endif
		}
	#endif
	
	#ifdef GPIO_PURE_LED1
		if (LED2value != (max > 0x80))
		{
			digitalWrite(GPIO_PURE_LED2, (max > 0x80));
			LED2value = (max > 0x80);
		}
		else
		{
			unchangedTimes++;
		#ifdef P9813DEBUG
			printf("Unchanged this time, %d\n", unchangedTimes);
		#endif
		}
	#endif
	
	#ifdef GPIO_PURE_LED3
		if (LED3value != (max > 0xC0))
		{
			digitalWrite(GPIO_PURE_LED3, (max > 0xC0));
			LED3value = (max > 0xC0);
		}
		else
		{
			unchangedTimes++;
		#ifdef P9813DEBUG
			printf("Unchanged this time, %d\n", unchangedTimes);
		#endif
		}
	#endif
#endif

	if ( (previousR != r) || (previousG != g) || (previousB != b) || (!unchangedTimes))
	{
		sendByte(0);sendByte(0);sendByte(0);sendByte(0);
		sendColor(r, g, b);
		sendByte(0);sendByte(0);sendByte(0);sendByte(0);
		previousR = r;
		previousG = g;
		previousB = b;
	}
	else
	{
		unchangedTimes++;
#ifdef P9813DEBUG
	printf("Unchanged this time, %d\n", unchangedTimes);
#endif
	}
	
} 

// Set the color to LED, or the first LED.
// This is not 'buffered', every time you invoke this method, it would send the signals directly to the bus.
// Advantage: What you see is what you want.
// Disadvantage: If you invoke this all the time, and write the same color, it costs a lot of CPU.
void setColorRGB(unsigned char r, unsigned char g, unsigned char b)
{
	sendByte(0);sendByte(0);sendByte(0);sendByte(0);
	sendColor(r, g, b);
	sendByte(0);sendByte(0);sendByte(0);sendByte(0);
	previousR = r;
	previousG = g;
	previousB = b;
} 

// Set the color with multiple LEDs.
// Not tested yet.
void setColorRGBs(unsigned char* r, unsigned char* g, unsigned char* b, int count)
{
	int i = 0;
	
	sendByte(0);sendByte(0);sendByte(0);sendByte(0);
	for ( i = 0; i < count; i++ )
	{
		printf("led %d color = %d,%d,%d\n",i,r[i], g[i], b[i]);
		sendColor(r[i], g[i], b[i]);
	}
	sendByte(0);sendByte(0);sendByte(0);sendByte(0);
} 

// Initializing
// I noted this because occasionally the light was brought up, and cannot be set.
// Because I rebooted the Pi, and forgot to set to OUTPUT direction.
void initialP9813GPIO()
{
	int result = wiringPiSetup();
	if (result < 0)
	{
		printf("wiringPi setup failed, are you root?\n");
		exit(1);
	}
	
	TIMCLOCKINTERVAL.tv_sec = 0;
	TIMCLOCKINTERVAL.tv_nsec = 20000L;
	
	pinMode(CLKPIN, OUTPUT);
	pinMode(DATPIN, OUTPUT);
	setColorRGB(0, 0, 0);

#ifdef GPIO_PURE_LED
	// use wiringPi pinout
	#ifdef GPIO_PURE_LED1
	pinMode(GPIO_PURE_LED1, OUTPUT);
	digitalWrite(GPIO_PURE_LED1, 0);
	printf("Set up wiringPi GPIO%d\n", GPIO_PURE_LED1);
	#endif
	
	#ifdef GPIO_PURE_LED2
	pinMode(GPIO_PURE_LED2, OUTPUT);
	digitalWrite(GPIO_PURE_LED2, 0);
	printf("Set up wiringPi GPIO%d\n", GPIO_PURE_LED2);
	#endif
	
	#ifdef GPIO_PURE_LED3
	pinMode(GPIO_PURE_LED3, OUTPUT);
	digitalWrite(GPIO_PURE_LED3, 0);
	printf("Set up wiringPi GPIO%d\n", GPIO_PURE_LED3);
	#endif
#endif

}

////////////////////////////////////
// These functions below are for testing alone. You can test this file only when changing 'LEDmain' to 'main'
////////////////////////////////////
/// Question: I do NOT want these functions to be called outside this file, how to do it?

#ifdef SINGLE_FILE_DEBUG
static int loop = 1;
void CtrlCBreak(int sig)
{
	signal(sig, SIG_IGN);
	loop = 0;
	signal(sig, SIG_DFL);
}


int LEDmain(int argc, const char* argv[])
{
	int result = 0;
	int nextColor;
	unsigned char nextR, nextG, nextB, colorR, colorG, colorB, maxDiff;
	result = wiringPiSetup();
	signal(SIGINT,CtrlCBreak);
	if (result < 0)
	{
		printf("wiringPi setup failed, are you root?\n");
		exit(1);
	}
	
	pinMode(CLKPIN, OUTPUT);
	pinMode(DATPIN, OUTPUT);
	
	setColorRGBbuffered(0, 0, 0);
	sleep(1);
	//sendColor(255, 0, 0);
	setColorRGBbuffered(255, 0, 0);
	sleep(1);
	//sendColor(0, 255, 0);
	setColorRGBbuffered(0, 255, 0);
	sleep(1);
	//sendColor(0, 0, 255);
	setColorRGBbuffered(0, 0, 255);
	sleep(1);
	
	while(loop)
	{
		if ((colorR == nextR) && (colorG == nextG) && (colorB == nextB))
		{
			nextColor = rand() & 0x00FFFFFF;
			nextR = (nextColor & 0x00FF0000) >> 16;
			nextG = (nextColor & 0x0000FF00) >> 8;
			nextB = (nextColor & 0x000000FF);
			//printf("nextColor is %dR, %dG, %dB\n", nextR, nextG, nextB);
		}
		else
		{
			// colorR = (color & 0x00FF0000) >> 16;
			// colorG = (color & 0x0000FF00) >> 8;
			// colorB = (color & 0x000000FF);
			
			maxDiff = 0;
			maxDiff = (maxDiff > abs(colorR - nextR)) ? maxDiff : abs(colorR - nextR);
			maxDiff = (maxDiff > abs(colorG - nextG)) ? maxDiff : abs(colorG - nextG);
			maxDiff = (maxDiff > abs(colorB - nextB)) ? maxDiff : abs(colorB - nextB);
			
			if (maxDiff == 0)
			{
				printf("Bug comes out,,,,,\n");
				break;
			}
			colorR = colorR - (colorR - nextR) / maxDiff;
			colorR = colorR & 0xFF;
			colorG = colorG - (colorG - nextG) / maxDiff;
			colorG = colorG & 0xFF;
			colorB = colorB - (colorB - nextB) / maxDiff;
			colorB = colorB & 0xFF;
		}
		
		setColorRGBbuffered(colorR, colorG, colorB);
		usleep(15000);
	}
	
	printf("End.\n");
	setColorRGBbuffered(0, 0, 0);
	
	return 0;
}
#endif