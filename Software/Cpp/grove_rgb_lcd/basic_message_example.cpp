#include "grove_rgb_lcd.h"
#include "grovepi.h"
#include <stdlib.h>
#include <stdio.h>

int main()
{
  GroveLCD lcd; // initialize new Grove LCD RGB device

  try{
      // connect to the i2c-line
      lcd.connect();

      // set text and RGB color on the LCD
      lcd.setText("Hello world\nThis is an LCD test");
      lcd.setRGB(0, 128, 64);

      // continuously change color for roughly 2.5 seconds
      for(int value = 0; value < 256; value ++)
      {
        lcd.setRGB(value, 255 - value, 0);
        delay(10);
      }
      // set final color
      lcd.setRGB(0, 255, 0);

      // and display a last minute text
      lcd.setText("Bye bye, this should wrap onto the next line");
  }
  catch (std::exception &e){

    // if any connection errors arise
    // throw runtime exception
    //
    printf(e.what());
  }

  return 0;
}
