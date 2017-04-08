// Copyright Dexter Industries, 2016
// http://dexterindustries.com/grovepi

#ifndef GROVEPI_H
#define GROVEPI_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
//#include <linux/i2c.h>
#include <unistd.h>
#include <linux/i2c-dev.h>
#include <fcntl.h>
#include <string.h>
#include <sys/ioctl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <stdbool.h>
#include <stdint.h>

const uint8_t INPUT = 0;
const uint8_t OUTPUT = 1;
const bool LOW = false;
const bool HIGH = true;
uint8_t ADDRESS = 0x04;


// default address of GrovePi set as default argument
bool initGrovePi(uint8_t address);
bool writeBlock(uint8_t command, uint8_t pin_number, uint8_t opt1 = 0, uint8_t opt2 = 0);
bool writeByte(uint8_t byte_val);
bool readBlock(uint8_t *data_block);
uint8_t readByte();

void piSleep(unsigned int milliseconds);
bool pinMode(uint8_t pin, uint8_t mode);
bool digitalWrite(uint8_t pin, bool value);
uint8_t digitalRead(uint8_t pin);
bool analogWrite(uint8_t pin, uint8_t value);
int analogRead(uint8_t pin);
int ultrasonicRead(uint8_t pin);

#endif
