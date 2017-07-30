## GrovePi Firmware version 1.2.6 - Mar 2016

GrovePi is an open source platform for connecting Grove Sensors to the Raspberry Pi.  [See more about the GrovePi here.](http://www.dexterindustries.com/grovepi)

##Changes in 1.2.6
* Support for Chainable RGB LED added
* Support for 433Mhz RF module added
* Ultrasonic sensor code updated

## Updating the firmware on your GrovePi
To Test the 1.2.6 firmware, make the installation script executable and run it 

First make the update script executable:

**sudo chmod +x install_test_firmware_software.sh**

then run it:

**sudo ./firmware_update.sh**

This will install the 1.2.6 firmware on the GrovePi and update the GrovePi python library. 
## Learn More

See more at the [GrovePi Site](http://www.GrovePi.com/)
[Dexter Industries](http://www.dexterindustries.com)

##Contributors
The following github users have contributed to the changes on the firmware and software:
* @tkumata
* @nikkoura
* @KillingJacky

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
THE SOFTWARE.


### Changes

* Adds Grove 433MHz simple link transmitter


### Commands

| name                                | byte1 | byte2    | byte3       | byte4        | description                                             |
|:----------------------------------- |:-----:|:-------- |:----------- |:------------ |:------------------------------------------------------- |
| Digital read                        | 1     | pin      | _unused_    | _unused_     | Read the value from a digital pin, either HIGH or LOW   |
| Digital write                       | 2     | pin      | value       | _unused_     | Write a HIGH or LOW to a digital pin                    |
| Analog read                         | 3     | pin      | _unused_    | _unused_     | Read the value from an analog pin                       |
| Analog write                        | 4     | pin      | value       | _unused_     | Writes an analog value (PWM wave) to a pin              |
| Pin mode                            | 5     | pin      | pin mode    | _unused_     | Configure a pin to behave either as input or output     |
| Ultrasonic read                     | 7     | pin      | _unused_    | _unused_     | Get the distance in cm                                  |
| Dust sensor read                    | 10    | _unused_ | _unused_    | _unused_     | Read the dust concentration in air                      |
| Encoder read                        | 11    | _unused_ | _unused_    | _unused_     | Read the encoder position                               |
| Flow read                           | 12    | _unused_ | _unused_    | _unused_     | Read the flow rate                                      |
| Flow disable                        | 13    | _unused_ | _unused_    | _unused_     | Disable the flow meter                                  |
| Dust sensor enable                  | 14    | _unused_ | _unused_    | _unused_     | Enable the dust sensor                                  |
| Dust sensor disable                 | 15    | _unused_ | _unused_    | _unused_     | Disable the dust sensor                                 |
| Encoder enable                      | 16    | _unused_ | _unused_    | _unused_     | Enable the encoder                                      |
| Encoder disable                     | 17    | _unused_ | _unused_    | _unused_     | Disable the encoder                                     |
| Flow enable                         | 18    | _unused_ | _unused_    | _unused_     | Enable the flow meter                                   |
| Accelerometer read                  | 20    | pin      | _unused_    | _unused_     | Get X, Y and Z from the 1.5g accelerometer              |
| RTC read                            | 30    | pin      | _unused_    | _unused_     | Get the time and date from the RTC                      |
| DHT read                            | 40    | pin      | dht type    | _unused_     | Read the temperature and humidity                       |
| LED bar init                        | 50    | pin      | orientation | _unused_     | Initialise a LED bar                                    |
| LED bar orientation                 | 51    | pin      | orientation | _unused_     | Set LED bar orientation                                 |
| LED bar set level                   | 52    | pin      | level       | _unused_     | Set LED bar level (0-10)                                |
| LED bar set single LED              | 53    | pin      | led         | state        | Set a single LED on the LED bar                         |
| LED bar toggle single LED           | 54    | pin      | led         | _unused_     | Toggle a single LED on the LED bar                      |
| LED bar set state                   | 55    | pin      | bits 1-8    | bits 9-10    | Set all LEDs on the LED bar                             |
| LED bar get state                   | 56    | pin      | _unused_    | _unused_     | Get the current state of the LEDs on the LED bar        |
| 4 digit init                        | 70    | pin      | _unused_    | _unused_     | Initialise a 4 digit display                            |
| 4 digit set brightness              | 71    | pin      | brightness  | _unused_     | Set brightness (0-7)                                    |
| 4 digit value without leading zeros | 72    | pin      | bits 1-8    | bits 9-16    | Right aligned decimal value without leading zeros       |
| 4 digit value with leading zeros    | 73    | pin      | bits 1-8    | bits 9-16    | Right aligned decimal value with leading zeros          |
| 4 digit set individual digit        | 74    | pin      | index       | number       | Display a number in one of the 4 segments               |
| 4 digit set individual segment      | 75    | pin      | index       | bits         | Set individual LEDs in one of the 4 segments            |
| 4 digit set scoreboard              | 76    | pin      | left number | right number | Set left and right numbers (0-99) with a colon          |
| 4 digit display analog read         | 77    | pin      | analog pin  | seconds      | Display analog read for n seconds, 4 samples per second |
| 4 digit display on                  | 78    | pin      | _unused_    | _unused_     | Turn the entire display on                              |
| 4 digit display off                 | 79    | pin      | _unused_    | _unused_     | Turn the entire display off                             |
| Store RGB color                     | 90    | red      | green       | blue         | Store a color for later use                             |
| Chainable RGB init                  | 91    | pin      | num leds    | _unused_     | Initialise a chain of one or more RGB LEDs              |
| Chainable RGB test pattern          | 92    | pin      | num leds    | test color   | Set all LEDs to white, red, green, blue, cyan, magenta, yellow or black using a combination of 3 RGB bits |
| Chainable RGB set LEDs with pattern | 93    | pin      | pattern     | which led    | Set color using pattern: 0 this LED only, 1: all except this, 2: this and all inwards, 3: this and all outwards |
| Chainable RGB set LEDs with modulo  | 94    | pin      | offset      | divisor      | Set color on all LEDs >= offset when mod remainder is 0 |
| Chainable RGB set level             | 95    | pin      | level       | reverse      | Set color on all LEDs <= level, outwards unless reverse |
| 433 MHz transmitter init            | 100   | 1        | pin         | _unused_     | Initialize transmitter                                  |
| 433 MHz transmitter set buffer size | 100   | 2        | size        | _unused_     | Prepare empty buffer to store message                   |
| 433 MHz transmitter transmit buffer | 100   | 3        | _unused_    | _unused_     | Transmit buffer contents                                |
| 433 MHz transmitter fill buffer     | 101   | byte 1   | byte 2      | byte 3       | Append 3 bytes to buffer                                |


### Library Dependencies

* [DHT](https://github.com/karan259/DHT-sensor-library)
* [MMA7660](https://github.com/mcauser/Grove-3Axis-Digital-Accelerometer-1.5g-MMA7660FC)
* [DS1307](https://github.com/Seeed-Studio/RTC_DS1307)
* [Grove_LED_bar](https://github.com/Seeed-Studio/Grove_LED_Bar)
* [TM1637](https://github.com/mcauser/TM1637-led-driver-7-segment)
* [Chainable_RGB_LED](https://github.com/mcauser/Grove-Chainable-RGB-LED)
* [VirtualWire](http://www.airspayce.com/mikem/arduino/VirtualWire/)
