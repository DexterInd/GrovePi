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

#include <Arduino.h>
#include "Grove_LED_Bar.h"

// Initialise
//Grove_LED_Bar::Grove_LED_Bar(unsigned char pinClock, unsigned char pinData, bool greenToRed)
void Grove_LED_Bar::begin(unsigned char pinClock, unsigned char pinData, bool greenToRed)
{
  __pinClock = pinClock;
  __pinData = pinData;
  __greenToRed = greenToRed;  // ascending or decending

  __state = 0x00;  // persist state so individual leds can be toggled

  pinMode(__pinClock, OUTPUT);
  pinMode(__pinData, OUTPUT);
}


// Send the latch command
void Grove_LED_Bar::latchData()
{
  digitalWrite(__pinData, LOW);
  delayMicroseconds(10);

  for (unsigned char i = 0; i < 4; i++)
  {
    digitalWrite(__pinData, HIGH);
    digitalWrite(__pinData, LOW);
  }
}


// Send 16 bits of data
void Grove_LED_Bar::sendData(unsigned int data)
{
  for (unsigned char i = 0; i < 16; i++)
  {
    unsigned int state = (data & 0x8000) ? HIGH : LOW;
    digitalWrite(__pinData, state);

    state = digitalRead(__pinClock) ? LOW : HIGH;
    digitalWrite(__pinClock, state);

    data <<= 1;
  }
}


// Change the orientation
// Green to red, or red to green
void Grove_LED_Bar::setGreenToRed(bool greenToRed)
{
  __greenToRed = greenToRed;

  setBits(__state);
}


// Set level (0-10)
// Level 0 means all leds off
// Level 10 means all leds on
void Grove_LED_Bar::setLevel(unsigned char level)
{
  level = max(0, min(10, level));

  // Set level number of bits from the left to 1
  __state = ~(~0 << level);

  setBits(__state);
}


// Set a single led
// led (1-10)
// state (0=off, 1=on)
void Grove_LED_Bar::setLed(unsigned char led, bool state)
{
  led = max(1, min(10, led));

  // Zero based index 0-9 for bitwise operations
  led--;

  // Bitwise OR or bitwise AND
  __state = state ? (__state | (0x01<<led)) : (__state & ~(0x01<<led));

  setBits(__state);
}


// Toggle a single led
// led (1-10)
void Grove_LED_Bar::toggleLed(unsigned char led)
{
  led = max(1, min(10, led));

  // Zero based index 0-9 for bitwise operations
  led--;

  // Bitwise XOR the leds current value
  __state ^= (0x01<<led);

  setBits(__state);
}


// Set the current state, one bit for each led
// 0    = 0x0   = 0b000000000000000 = all leds off
// 5    = 0x05  = 0b000000000000101 = leds 1 and 3 on, all others off
// 341  = 0x155 = 0b000000101010101 = leds 1,3,5,7,9 on, 2,4,6,8,10 off
// 1023 = 0x3ff = 0b000001111111111 = all leds on
//                       |        |
//                       10       1
void Grove_LED_Bar::setBits(unsigned int bits)
{
  __state = bits & 0x3FF;

  sendData(CMDMODE);

  for (unsigned char i = 0; i < 10; i++)
  {
    if (__greenToRed)
    {
      // Bitwise AND the 10th bit (0x200) and left shift to cycle through all bits
      sendData((bits << i) & 0x200 ? ON : OFF);
    }
    else
    {
      // Bitwise AND the 1st bit (0x01) and right shift to cycle through all bits
      sendData((bits >> i) & 0x01 ? ON : OFF);
    }
  }

  // Two extra empty bits for padding the command to the correct length
  sendData(0x00);
  sendData(0x00);

  latchData();
}


// Return the current state
unsigned int Grove_LED_Bar::getBits()
{
  return __state;
}

// Has this instance been initialised?
bool Grove_LED_Bar::ready()
{
  return __pinClock != 0;
}
