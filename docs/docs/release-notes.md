# Release Notes For the Firmware

## Maintenance Team

The current and past members of the GrovePi team in alphabetical order are:

- [@CleoQc](https://github.com/CleoQc)
- [@johnisanerd](https://github.com/johnisanerd)
- [@karan259](https://github.com/karan259)
- [@RobertLucian](https://github.com/RobertLucian)

Also, we have a couple of notable contributors to the GrovePi but for other libraries:

- [@marcellobarile](https://github.com/marcellobarile) for the NodeJS library
- [@mcauser](https://github.com/mcauser) for adding different new functionalities/bug fixes/examples to our current library
- [@lanselambor](https://github.com/lanselambor)
- [@nikkoura](https://github.com/nikkoura)
- [@lucavallin](https://github.com/lucavallin) for coming with fixes to the Go library
- [@rpedersen](https://github.com/rpedersen) for C# stuff
- [@k33g](https://github.com/k33g) for Java library

## Version 1.4.0 - 27 April 2019

- Add support for setting up interrupt events on each digital port of the GrovePi, thus breaking the limit of just two available hardware interrupts [#446](https://github.com/DexterInd/GrovePi/pull/446)
- Enable the Grove Dust Sensor, the Grove Encoder and the Grove Flow Meter to work on any digital port of the GrovePi and support 7 or 3 or respectively 7 devices at the same time [#446](https://github.com/DexterInd/GrovePi/pull/446)

## [Version 1.3.0](https://github.com/DexterInd/GrovePi/projects/2) - 1 Aug 2018

- Fixed synchronization bugs which led to very small IO rates

    - Also caused values to overlap on other ports [#412](https://github.com/DexterInd/GrovePi/issues/412)
    - Caused I2C errors when functions were called with no delay between them [#409](https://github.com/DexterInd/GrovePi/issues/409)

- Small refactorization of the code to something slightly better
- Fixed the dust sensor [#408](https://github.com/DexterInd/GrovePi/issues/408)
- Mitigated abnormality caused by the Raspberry Pi not supporting clock stretching on the I2C [#411](https://github.com/DexterInd/GrovePi/issues/411)
- Debugged and sped up the rate of acquisition of the DHT sensor [#418](https://github.com/DexterInd/GrovePi/issues/418)
- Add IR receiver functionality for any remote control and fix inherent issues with the library [#416](https://github.com/DexterInd/GrovePi/issues/416)
- Add option to set the flow meter and the dust sensor on different ports other than D2 [#421](https://github.com/DexterInd/GrovePi/issues/421)

## Version 1.2.7 - 20 Dec 2016

-  Faster IO
-  Less IO Errors
-  RTC and MMA7xxx accelerometer code removed from the firmware

## Version 1.2.2 - 22 Jan 2015

- Grove Chainable RGB LED added
- Ability to persist a RGB color in memory for later use

## Version 1.2.1 - 30 Dec 2014

- Grove 4 Digit Display added

## Version 1.2.0 - 29 Dec 2014

- Grove LED Bar added
- Firmware version made available

## Version 1.1 - 13 Feb 2014

- DHT, ultrasonic, RTC code added
- Support for multiple modules for same type added (Not tested)
- Protocol made more robust
