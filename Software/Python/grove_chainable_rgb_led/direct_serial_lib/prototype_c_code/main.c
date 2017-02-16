/*
This one is to read RFID card by PN532 through SPI, respond to LED lights(P9813) and a beeper

Input:	PN532(SPI)
Output:	P9813, GPIO 1 port 

NFC module:	http://www.seeedstudio.com/wiki/NFC_Shield_V2.0
LED light:	http://www.seeedstudio.com/wiki/Grove_-_Chainable_RGB_LED
beeper:		http://item.taobao.com/item.htm?spm=0.0.0.0.A0Zkth&id=6859691900


Outline:
Repeatedly read from NFC, use cardID to identify,	// currently I don't know how to read the blocks.
if it matches some fixed number, it shows white light and beepGPIO;
if it matches another number, the program exits.
otherwise, it gradually dim the light.

You need the wiringPi lib.

Compile: 
make

Run:
sudo ./NFClight


Thanks the following persons developed the libs which this project used.
wiringPi lib from:	Gordons Projects @ https://projects.drogon.net/raspberry-pi/wiringpi/
nfc lib from:		Katherine @ http://blog.iteadstudio.com/to-drive-itead-pn532-nfc-module-with-raspberry-pi/

This project is created by @DaochenShi (shidaochen@live.com)

20140322 maintaince:
	LED init and control should be done by P9813GPIO, so any LED init related are removed from this file. Go check P9813GPIO.c
*/


#include "PN532SPI.h"

#include <stdio.h>
#include <unistd.h>	// for usleep
#include <signal.h>	// for SIG_IGN etc.
#include <fcntl.h>	// for O_WRONLY
#include <errno.h>	// for errno
#include <time.h>	// for clock()
#include <pthread.h>	// for multithreading

//#define DEBUG_COLOR

//#define BEEPER_GPIO_PIN	6

int initialWiringPi();

void break_program(int sig);
void* adjust_color();
//#define MAXWAITINGTIME 10
static int loopingStatus = 0;
static unsigned char colorBase[3];
static unsigned char colorTarget[3];

//gcc main.c -lwiringPi P9813GPIO.h P9813GPIO.c

void rgbcycle(void)
{
	int i=0;
	while (1)
	{
	i++;
	if (i>255)
		i=0;
	setColorRGBbuffered(0,0,1);
	printf("color = %d\n",i);
	usleep(20 * 1000);

	}
}

int main(int argc, const char* argv[])
{

	unsigned char r[]={255,0,0};
	unsigned char g[]={0,255,0};
	unsigned char b[]={0,0,255};
	int i;
	// NFC related, the read card ID. Currently I can only read this. I don't know how to get other infos.
	// uint32_t cardID;
	// int allowFailureTimes = 2;

	// // run this program in background when not in Debug mode
// #ifndef DEBUG
	// {
		// pid_t pid, sid;
		// pid = fork();
		// if (pid < 0)
		// {
			// exit(EXIT_FAILURE);
		// }
		// if (pid > 0)
		// {
			// exit(EXIT_SUCCESS);
		// }
		
		// // change file mode mask
		// umask(0);
		// // open logs,,, but I did not record any logs
		
		// // create SID for child process
		// sid = setsid();
		// if (sid < 0)
		// {
			// exit(EXIT_FAILURE);
		// }
		
		// close(STDIN_FILENO);
		// close(STDOUT_FILENO);
		// //close(STDERR_FILENO);
	// }
// #endif	
	
	initialWiringPi();
	// pthread_t _colorThread;
	// loopingStatus = 1;
	// pthread_create(&_colorThread, NULL, adjust_color, NULL);
	// adjust_color();
	printf("All initialized...\n");
	// adjust_color();
	// setColorRGB(0, 0, 0);
	// rgbcycle();
	setColorRGBs(&r[0],&g[0],&b[0],3);
	for ( i = 0; i < 3; i++ )
	{
		printf("led %d color = %d,%d,%d\n",i,r[i], g[i], b[i]);
	}
	// while(loopingStatus)
	// {
// #ifdef DEBUG
	// printf("waiting for card read...\n");
// #endif

		// cardID = readPassiveTargetID(PN532_MIFARE_ISO14443A);

		// if ( cardID == 0 && allowFailureTimes > 0) 
		// {
			// allowFailureTimes--;
			// continue;
		// }
		// if ( cardID != 0 )
		// {
			// allowFailureTimes = 2;
			// if ((cardID % 256) ==  authCID)
			// {
				// colorBase[0] = 0xFF; colorBase[1] = 0xFF; colorBase[2] = 0xFF;
				// colorTarget[0] = 0xFF; colorTarget[1] = 0xFF; colorTarget[2] = 0xFF; 
				// setColorRGBbuffered(colorBase[0], colorBase[1], colorBase[2]);
			// }
			// else
			// {
				// if ((cardID % 256) == exitCID)
				// {
					// loopingStatus = 0;
					// break;
				// }
			// colorTarget[0] = (cardID >> 16) % 256;
			// colorTarget[1] = (cardID >> 8) % 256;
			// colorTarget[2] = cardID % 256; 
// #ifdef DEBUG
	// printf("cardID = %X\n", cardID);
// #endif
			// }
		// }
		// else
		// {
		// // allowFailureTimes < 0 and cardID == 0, which means no card.
// #ifdef DEBUG
	// printf("no card\n");
// #endif
			// colorTarget[0] = 0; colorTarget[1] = 0; colorTarget[2] = 0; 
		// }
		// sleep(1);

	// }
	// colorTarget[0] = 0; colorTarget[1] = 0; colorTarget[2] = 0; 
	// colorBase[0] = 2; colorBase[1] = 3; colorBase[2] = 6;
	// setColorRGB(10, 7, 6);
// #ifdef BEEPER_GPIO_PIN
	// digitalWrite(BEEPER_GPIO_PIN, 1);
	// usleep(100 * 1000);
	// digitalWrite(BEEPER_GPIO_PIN, 0);
// #endif
	// sleep(1);
	// setColorRGB(0, 0, 0);
	
	// pthread_join(_colorThread, NULL);
	// return 0;
}

// Set-up some necessary wiringPi and devices.
int initialWiringPi()
{
#ifdef DEBUG
	printf("Initializing.\n");
#endif

	// uint32_t nfcVersion;
	
	// First to setup wiringPi
	if (wiringPiSetup() < 0)
	{
		fprintf(stderr, "Unable to setup wiringPi: %s \n", strerror(errno));
		exit(1);
	}
#ifdef DEBUG
	printf("Set wiringPi.\n");
#endif


	// Initializing LEDs
	initialP9813GPIO();

	// Hook crtl+c event
	signal(SIGINT, break_program);
#ifdef DEBUG
	printf("Hooked Ctrl+C.\n");
#endif

// #ifdef BEEPER_GPIO_PIN
	// pinMode(BEEPER_GPIO_PIN, OUTPUT);
	// digitalWrite(BEEPER_GPIO_PIN, 1);
	// usleep(100 * 1000);
	// digitalWrite(BEEPER_GPIO_PIN, 0);
// #endif
	// // Use init function from nfc.c
	// // why you use such a simple function name?!
	// initialPN532SPI();
// #ifdef DEBUG
	// printf("NFC initialized begin().\n");
// #endif
	// nfcVersion = getFirmwareVersion();
	// if (!nfcVersion)
	// {
		// fprintf(stderr, "Cannot find PN53x board after getFirmwareVersion.\n");
		// exit(1);
	// }

	// SAMConfig();
	
	
#ifdef DEBUG
	printf("Initialized.\n");
#endif
	return 0;
}

// Accept Ctrl+C command, this seems not work when main process is forked.
void break_program(int sig)
{
	signal(sig, SIG_IGN);
	loopingStatus = 0;
	printf("Program end.\n");
	signal(sig, SIG_DFL);
}

// static clock_t previousTimeClock;
// Adjust the P9813 color by another thread.
void* adjust_color(void)
{
	// LED related	
	int colorMaxDiff;
	while (1){
		/// Parse current color, and gradually fade-in/fade-out

		printf("Changing color...loop = %d\n", loopingStatus);

		colorMaxDiff = 0;
		colorMaxDiff = (colorMaxDiff > abs(colorBase[0] - colorTarget[0])) ? colorMaxDiff : abs(colorBase[0] - colorTarget[0]);
		colorMaxDiff = (colorMaxDiff > abs(colorBase[1] - colorTarget[1])) ? colorMaxDiff : abs(colorBase[1] - colorTarget[1]);
		colorMaxDiff = (colorMaxDiff > abs(colorBase[2] - colorTarget[2])) ? colorMaxDiff : abs(colorBase[2] - colorTarget[2]);
		

		colorMaxDiff = (colorMaxDiff > 15) ? colorMaxDiff/16 : colorMaxDiff;

		if (colorMaxDiff)
		{
			{
				colorBase[0] = colorBase[0] - (colorBase[0] - colorTarget[0]) / colorMaxDiff;
				colorBase[1] = colorBase[1] - (colorBase[1] - colorTarget[1]) / colorMaxDiff;
				colorBase[2] = colorBase[2] - (colorBase[2] - colorTarget[2]) / colorMaxDiff;
				setColorRGBbuffered(colorBase[0], colorBase[1], colorBase[2]);
			}

	// printf("interval of previous %d\n", (clock() - previousTimeClock));
	// previousTimeClock = clock();
	printf("colorMaxDiff = %d, %dR->%dR, %dG->%dG, %dB->%dB\n",
		colorMaxDiff,
		colorBase[0], colorTarget[0],
		colorBase[1], colorTarget[1],
		colorBase[2], colorTarget[2]);

		}
		usleep(20 * 1000);

	}
}
