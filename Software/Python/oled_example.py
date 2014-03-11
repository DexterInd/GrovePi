#Example for grove OLED running directly from Raspberry Pi
from grove_oled import *

oled_init()
oled_clearDisplay()
oled_setNormalDisplay()
oled_setVerticalMode()
time.sleep(.1)

for i in range(0,12):
	oled_setTextXY(i,0)
	oled_putString("Hello World")