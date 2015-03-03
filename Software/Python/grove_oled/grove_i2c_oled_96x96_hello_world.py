# Example for Grove OLED 96x96 running directly from Raspberry Pi

# GrovePi + Grove OLED Display 96*96
# http://www.seeedstudio.com/wiki/Grove_-_OLED_Display_1.12%22

# Connect the OLED to any I2C port eg. I2C-1
# Can be found at I2C address 0x3c

from grove_oled import *

oled_init()
oled_clearDisplay()
oled_setNormalDisplay()
oled_setVerticalMode()
time.sleep(.1)

for i in range(0,12):
    oled_setTextXY(i,0)
    oled_putString("Hello World")
