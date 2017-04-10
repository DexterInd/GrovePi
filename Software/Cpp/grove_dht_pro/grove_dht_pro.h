#ifndef GROVE_RGB_LCD_H
#define GROVE_RGB_LCD_H

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <linux/i2c-dev.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <stdint.h>
#include <stdexcept>

#include "grovepi.h"

class GroveDHT
{
public:

const static uint8_t BLUE_MODULE = 0;
const static uint8_t WHITE_MODULE = 1;

GroveDHT(const uint8_t _module_type = BLUE_MODULE, const uint8_t _pin = 4);

void connect();
bool isConnected();
void getReadings(float &temp, float &humidity);

private:

uint8_t DEVICE_FILE;
uint8_t pin;
uint8_t module_type;
bool connected;
const static uint8_t DHT_TEMP_CMD = 40;
static char default_error_message[64];

static float fourBytesToFloat(uint8_t *data);

};


#endif
