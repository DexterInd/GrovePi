## GrovePi Firmware version 1.2 - Dec 2014

Binary sketch size: 10,226 bytes (of a 32,256 byte maximum)

### Changes

* Adds Grove LED Bar


### Commands

| name                      | byte1 | byte2    | byte3       | byte4     | description                                           |
|:------------------------- |:-----:|:-------- |:----------- |:--------- |:----------------------------------------------------- |
| Digital read              | 1     | pin      | _unused_    | _unused_  | Read the value from a digital pin, either HIGH or LOW |
| Digital write             | 2     | pin      | value       | _unused_  | Write a HIGH or LOW to a digital pin                  |
| Analog read               | 3     | pin      | _unused_    | _unused_  | Read the value from an analog pin                     |
| Analog write              | 4     | pin      | value       | _unused_  | Writes an analog value (PWM wave) to a pin            |
| Pin mode                  | 5     | pin      | pin mode    | _unused_  | Configure a pin to behave either as input or output   |
| Ultrasonic read           | 7     | pin      | _unused_    | _unused_  | Get the distance in cm                                |
| Firmware version          | 8     | _unused_ | _unused_    | _unused_  | Get the firmware version                              |
| Accelerometer read        | 20    | pin      | _unused_    | _unused_  | Get X, Y and Z from the 1.5g accelerometer            |
| RTC read                  | 30    | pin      | _unused_    | _unused_  | Get the time and date from the RTC                    |
| DHT read                  | 40    | pin      | dht type    | _unused_  | Read the temperature and humidity                     |
| LED bar init              | 50    | pin      | orientation | _unused_  | Initialise a LED bar                                  |
| LED bar orientation       | 51    | pin      | orientation | _unused_  | Set LED bar orientation                               |
| LED bar set level         | 52    | pin      | level       | _unused_  | Set LED bar level (0-10)                              |
| LED bar set single LED    | 53    | pin      | led         | state     | Set a single LED on the LED bar                       |
| LED bar toggle single LED | 54    | pin      | led         | _unused_  | Toggle a single LED on the LED bar                    |
| LED bar set state         | 55    | pin      | bits 1-8    | bits 9-10 | Set all LEDs on the LED bar                           |
| LED bar get state         | 56    | pin      | _unused_    | _unused_  | Get the current state of the LEDs on the LED bar      |


### Library Dependencies

* [DHT](https://github.com/karan259/DHT-sensor-library)
* [MMA7660](https://github.com/mcauser/Grove-3Axis-Digital-Accelerometer-1.5g-MMA7660FC)
* [DS1307](https://github.com/Seeed-Studio/RTC_DS1307)
* [Grove_LED_bar](https://github.com/Seeed-Studio/Grove_LED_Bar)
