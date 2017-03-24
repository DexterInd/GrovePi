## GrovePi Firmware version 1.2.7 - Dec 2016
'''
## License

The MIT License (MIT)

GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
Copyright (C) 2017  Dexter Industries

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
'''
Binary sketch size: 14,504 bytes (of a 32,256 byte maximum)

### Changes

* Faster IO (upto 300 reads/writes a second)
* Less IO Errors
* Support for RTC and MMA7xxx accelerometer removed from firmware and moved to Software

### Installation
* First run DI update from the Desktop. (If you are not running Raspbian for Robots, first update the GrovePi git repository, then run setup.py from [here](https://github.com/DexterInd/GrovePi/tree/master/Software/Python to update the grovepi python library): **sudo python setup.py install**
* Next run the firmware update script for v1.2.7.
* Go to the fimrware 1.2.7 folder [here] https://github.com/DexterInd/GrovePi/tree/master/Firmware/Source/v1.2/grove_pi_v1_2_7)
* Make the firmware update script executable: **sudo chmod +x firmware_update_1_2_7.sh**
* then run it: **sudo ./firmware_update_1_2_7.sh**
* After this, run the firmware check script [here]( https://github.com/DexterInd/GrovePi/blob/master/Software/Python/grove_firmware_version_check.py) to make sure that you are running 1.2.7. 

In case of any problems with the firmware, just run the firmware update [here](https://github.com/karan259/GrovePi/tree/master/Firmware) to go back to the stable firmware and report the problems on the [forums](http://forum.dexterindustries.com/c/grovepi)

### Commands

I2C address: 0x4

| name                                | byte1 | byte2    | byte3       | byte4        | response           | description                                             |
|:----------------------------------- |:-----:|:-------- |:----------- |:------------ |:------------------ |:------------------------------------------------------- |
| Digital read                        | 1     | pin      | _unused_    | _unused_     | 0 or 1             | Read the value from a digital pin, either HIGH or LOW   |
| Digital write                       | 2     | pin      | value       | _unused_     | _none_             | Write a HIGH or LOW to a digital pin                    |
| Analog read                         | 3     | pin      | _unused_    | _unused_     | _unused_, msb, lsb | Read the value from an analog pin                       |
| Analog write                        | 4     | pin      | value       | _unused_     | _none_             | Writes an analog value (PWM wave) to a pin              |
| Pin mode                            | 5     | pin      | pin mode    | _unused_     | _none_             | Configure a pin to behave either as input or output     |
| Ultrasonic read                     | 7     | pin      | _unused_    | _unused_     | _unused_, msb, lsb | Get the distance in cm                                  |
| Firmware version                    | 8     | _unused_ | _unused_    | _unused_     | _unused_, 1, 2, 7  | Get the firmware version                                |
| Accelerometer read                  | 20    | pin      | _unused_    | _unused_     | _unused_, x, y, z  | Get X, Y and Z from the 1.5g accelerometer (-31 to 32)  |
| RTC read                            | 30    | pin      | _unused_    | _unused_     | _unused_, 8 bytes  | Get the time and date from the RTC                      |
| DHT read                            | 40    | pin      | dht type    | _unused_     | _unused_, temp, humidity | Read the temperature and humidity. dht_type: 0: DHT11, 1: DHT22, 2: DHT21, 3: AM2301 |
| LED bar init                        | 50    | pin      | orientation | _unused_     | _none_             | Initialise a LED bar                                    |
| LED bar orientation                 | 51    | pin      | orientation | _unused_     | _none_             | Set LED bar orientation                                 |
| LED bar set level                   | 52    | pin      | level       | _unused_     | _none_             | Set LED bar level (0-10)                                |
| LED bar set single LED              | 53    | pin      | led         | state        | _none_             | Set a single LED on the LED bar                         |
| LED bar toggle single LED           | 54    | pin      | led         | _unused_     | _none_             | Toggle a single LED on the LED bar                      |
| LED bar set state                   | 55    | pin      | bits 1-8    | bits 9-10    | _none_             | Set all LEDs on the LED bar                             |
| LED bar get state                   | 56    | pin      | _unused_    | _unused_     | _unused_, lsb, msb | Get the current state of the LEDs on the LED bar        |
| 4 digit init                        | 70    | pin      | _unused_    | _unused_     | _none_             | Initialise a 4 digit display                            |
| 4 digit set brightness              | 71    | pin      | brightness  | _unused_     | _none_             | Set brightness (0-7)                                    |
| 4 digit value without leading zeros | 72    | pin      | bits 1-8    | bits 9-16    | _none_             | Right aligned decimal value without leading zeros       |
| 4 digit value with leading zeros    | 73    | pin      | bits 1-8    | bits 9-16    | _none_             | Right aligned decimal value with leading zeros          |
| 4 digit set individual digit        | 74    | pin      | index       | number       | _none_             | Display a number in one of the 4 segments               |
| 4 digit set individual segment      | 75    | pin      | index       | bits         | _none_             | Set individual LEDs in one of the 4 segments            |
| 4 digit set scoreboard              | 76    | pin      | left number | right number | _none_             | Set left and right numbers (0-99) with a colon          |
| 4 digit display analog read         | 77    | pin      | analog pin  | seconds      | _none_             | Display analog read for n seconds, 4 samples per second |
| 4 digit display on                  | 78    | pin      | _unused_    | _unused_     | _none_             | Turn the entire display on                              |
| 4 digit display off                 | 79    | pin      | _unused_    | _unused_     | _none_             | Turn the entire display off                             |
| Store RGB color                     | 90    | red      | green       | blue         | _none_             | Store a color for later use                             |
| Chainable RGB init                  | 91    | pin      | num leds    | _unused_     | _none_             | Initialise a chain of one or more RGB LEDs              |
| Chainable RGB test pattern          | 92    | pin      | num leds    | test color   | _none_             | Set all LEDs to white, red, green, blue, cyan, magenta, yellow or black using a combination of 3 RGB bits |
| Chainable RGB set LEDs with pattern | 93    | pin      | pattern     | which led    | _none_             | Set color using pattern: 0 this LED only, 1: all except this, 2: this and all inwards, 3: this and all outwards |
| Chainable RGB set LEDs with modulo  | 94    | pin      | offset      | divisor      | _none_             | Set color on all LEDs >= offset when mod remainder is 0 |
| Chainable RGB set level             | 95    | pin      | level       | reverse      | _none_             | Set color on all LEDs <= level, outwards unless reverse |


### Library Dependencies

* [DHT](https://github.com/karan259/DHT-sensor-library)
* [MMA7660](https://github.com/mcauser/Grove-3Axis-Digital-Accelerometer-1.5g-MMA7660FC)
* [DS1307](https://github.com/Seeed-Studio/RTC_DS1307)
* [Grove_LED_bar](https://github.com/Seeed-Studio/Grove_LED_Bar)
* [TM1637](https://github.com/mcauser/TM1637-led-driver-7-segment)
* [Chainable_RGB_LED](https://github.com/mcauser/Grove-Chainable-RGB-LED)
