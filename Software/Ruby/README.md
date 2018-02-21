# Ruby support for GrovePi

## Introduction
This ruby module adds support for using GrovePi with Ruby.

A set of examples can be found in the **tests** directory.
Check them out for usage.

## Dependencies
* Ruby version above 2.0 is required.
* The Ruby module **i2c-devices** must be installed, ```# gem install i2c-devices```.

## Current State
As the initial state of this module the following features are implemented and tested:

* Analog read on ports A0, A1 and A2.
* Analog write with PWM on ports D3, D5 and D6.
* Digital read/write on ports D2 through D8.
* Read/write data to I2C slave devices present on ports I2C-1, I2C-2 or I2C-3.
* Tested on Raspberry Pi 3, Model B and Raspberry Pi, Model B, Rev 2
  with Raspbian version: November 2017 and GrovePi+ with firmware version: 1.2.7.

## Todo

* Implement rest of the commands that are supported by the firmware.
* Windows IoT core support.
* More testing.
