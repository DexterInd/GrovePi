// Copyright Dexter Industries, 2016
// http://dexterindustries.com/grovepi

#ifndef GROVEPI_H
#define GROVEPI_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <linux/i2c-dev.h>
#include <fcntl.h>
#include <string.h>
#include <sys/ioctl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <stdbool.h>
#include <stdint.h>

static const bool DEBUG = false;
const unsigned int RBUFFER_SIZE = 32;
const unsigned int WBUFFER_SIZE = 5;

static char smbus_name[11];
static int file_device = NULL;

const unsigned int DIGITAL_READ = 1;
const unsigned int DIGITAL_WRITE = 2;
const unsigned int ANALOG_READ = 3;
const unsigned int ANALOG_WRITE = 4;
const unsigned int PIN_MODE = 5;
const unsigned int USONIC_READ = 6;
const unsigned int INPUT = 0;
const unsigned int OUTPUT = 1;
uint8_t ADDRESS = 0x04;

static unsigned int gpioHardwareRevision();
static char* SMBusName();

// default address of GrovePi set as default argument
bool initGrovePi(uint8_t address);
bool writeBlock(uint8_t command, uint8_t pin_number, uint8_t opt1, uint8_t opt2);
bool writeByte(uint8_t byte_val);
bool readBlock(uint8_t *data_block);
uint8_t readByte();

void piSleep(unsigned int milliseconds);
bool pinMode(uint8_t pin, uint8_t mode);
bool digitalWrite(uint8_t pin, uint8_t value);
uint8_t digitalRead(uint8_t pin);
bool analogWrite(uint8_t pin, uint8_t value);
int analogRead(uint8_t pin);
int ultrasonicRead(uint8_t pin);

#endif
