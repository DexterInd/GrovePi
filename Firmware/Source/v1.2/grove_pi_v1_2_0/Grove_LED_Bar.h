/*
  LED bar library V2.0
  2010 Copyright (c) Seeed Technology Inc.  All right reserved.

  Original Author: LG

  Modify: Loovee, 2014-2-26
  User can choose which Io to be used.

  This library is free software; you can redistribute it and/or
  modify it under the terms of the GNU Lesser General Public
  License as published by the Free Software Foundation; either
  version 2.1 of the License, or (at your option) any later version.

  This library is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
  Lesser General Public License for more details.

  You should have received a copy of the GNU Lesser General Public
  License along with this library; if not, write to the Free Software
  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
*/

#ifndef Grove_LED_Bar_H
#define Grove_LED_Bar_H

#define CMDMODE 0x00  // Work on 8-bit mode
#define ON      0xff  // 8-bit 1 data
#define OFF     0x00  // 8-bit 0 data

class Grove_LED_Bar
{

private:

  unsigned int __pinClock;  // Clock pin
  unsigned int __pinData;   // Data pin
  bool __greenToRed;        // Orientation (0 = red to green, 1 = green to red)
  unsigned int __state;     // Led state

  void sendData(unsigned int data);  // Send a word to led bar
  void latchData(void);              // Load data into the latch register

public:

  //Grove_LED_Bar(unsigned char pinClock, unsigned char pinData, bool greenToRed);  // Initialize
  void begin(unsigned char pinClock, unsigned char pinData, bool greenToRed);  // Initialize

  void setGreenToRed(bool greenToRed);         // (Re)set orientation
  void setLevel(unsigned char level);          // Set level
  void setLed(unsigned char led, bool state);  // Set a single led
  void toggleLed(unsigned char led);           // Toggle a single led
  void setBits(unsigned int bits);             // Toggle leds to match given bits
  unsigned int getBits();                      // Get the current state
  bool ready();                                // Has this instance been initialised?
};

#endif
