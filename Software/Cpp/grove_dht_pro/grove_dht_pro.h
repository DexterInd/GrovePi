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
#include <cmath>

#include "grovepi.h"

namespace GrovePi
{
  class DHT
  {
	  public:

		  const static uint8_t BLUE_MODULE = 0;
		  const static uint8_t WHITE_MODULE = 1;

		  DHT(const uint8_t _module_type = BLUE_MODULE, const uint8_t _pin = 4)
			  : module_type(_module_type), pin(_pin) {
		  }

		  void init();
		  void getSafeData(float &temp, float &humidity);
		  void getUnsafeData(float &temp, float &humidity);

	  private:

		  uint8_t DEVICE_FILE; // I2C device file
		  const uint8_t module_type;
		  const uint8_t pin;
		  const static uint8_t DHT_TEMP_CMD = 40; // command for reaching DTH sensor on the GrovePi
		  const static int MAX_RETRIES = 3;

		  // converts the first 4 bytes of the array
		  // into a float
		  static const float fourBytesToFloat(uint8_t *data);
		  static const bool areGoodReadings(int temp, int humidity);

  };
}


#endif
