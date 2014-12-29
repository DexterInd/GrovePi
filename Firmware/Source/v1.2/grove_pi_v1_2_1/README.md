## GrovePi Firmware version 1.2.1 - Dec 2014

Binary sketch size: 12,236 bytes (of a 32,256 byte maximum)

### Changes

* Adds Grove 4 Digit Display


### Commands

| name                                | byte1 | byte2    | byte3       | byte4        | description                                             |
|:----------------------------------- |:-----:|:-------- |:----------- |:------------ |:------------------------------------------------------- |
| Digital read                        | 1     | pin      | _unused_    | _unused_     | Read the value from a digital pin, either HIGH or LOW   |
| Digital write                       | 2     | pin      | value       | _unused_     | Write a HIGH or LOW to a digital pin                    |
| Analog read                         | 3     | pin      | _unused_    | _unused_     | Read the value from an analog pin                       |
| Analog write                        | 4     | pin      | value       | _unused_     | Writes an analog value (PWM wave) to a pin              |
| Pin mode                            | 5     | pin      | pin mode    | _unused_     | Configure a pin to behave either as input or output     |
| Ultrasonic read                     | 7     | pin      | _unused_    | _unused_     | Get the distance in cm                                  |
| Firmware version                    | 8     | _unused_ | _unused_    | _unused_     | Get the firmware version                                |
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

### Library Dependencies

* [DHT](https://github.com/karan259/DHT-sensor-library)
* [MMA7660](https://github.com/mcauser/Grove-3Axis-Digital-Accelerometer-1.5g-MMA7660FC)
* [DS1307](https://github.com/Seeed-Studio/RTC_DS1307)
* [Grove_LED_bar](https://github.com/Seeed-Studio/Grove_LED_Bar)
* [TM1637](https://github.com/mcauser/TM1637-led-driver-7-segment)
