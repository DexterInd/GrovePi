This one is to read RFID card by PN532 through SPI, respond to LED lights(P9813) and a beeper

Input:	PN532(SPI)
Output:	P9813, GPIO 1 port 

NFC module:	http://www.seeedstudio.com/wiki/NFC_Shield_V2.0

LED light:	http://www.seeedstudio.com/wiki/Grove_-_Chainable_RGB_LED

beeper:		http://item.taobao.com/item.htm?spm=0.0.0.0.A0Zkth&id=6859691900


Outline:
Repeatedly read from NFC, use cardID to identify,	// currently I don't know how to read the blocks.
if it matches some fixed number, it shows green light and beepGPIO;
otherwise, it shows red and beepGPIO another sound.

You need the wiringPi lib.

Compile: 
make

Run:
sudo ./NFClight


Thanks the following persons developed the libs which this project used.
wiringPi lib from:	Gordons Projects @ https://projects.drogon.net/raspberry-pi/wiringpi/
nfc lib from:		Katherine @ http://blog.iteadstudio.com/to-drive-itead-pn532-nfc-module-with-raspberry-pi/

This project is created by @DaochenShi (shidaochen@live.com)

