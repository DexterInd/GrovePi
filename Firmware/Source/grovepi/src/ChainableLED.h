/*
Copyright (C) 2012 Paulo Marques (pjp.marques@gmail.com)

Permission is hereby granted, free of charge, to any person obtaining a copy of 
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all 
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN 
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/

/* 
 * Library for controlling a chain of RGB LEDs based on the P9813 protocol.
 * E.g., supports the Grove Chainable RGB LED product.
 *
 * Information about the P9813 protocol obtained from:
 * http://www.seeedstudio.com/wiki/index.php?title=Twig_-_Chainable_RGB_LED
 */



#ifndef __ChainableLED_h__
#define __ChainableLED_h__

#include "Arduino.h"

#define _CL_RED             0
#define _CL_GREEN           1
#define _CL_BLUE            2
#define _CLK_PULSE_DELAY    20

class ChainableLED
{
public:
    // ChainableLED(byte clk_pin, byte data_pin, byte number_of_leds);
    void begin(byte clk_pin, byte data_pin, byte number_of_leds);
    // ~begin();
    
    void setColorRGB(byte led, byte red, byte green, byte blue);
    //void setColorHSB(byte led, float hue, float saturation, float brightness);
    
    byte getNumLeds();
    bool ready();

private:
    byte _clk_pin;
    byte _data_pin;
    byte _num_leds; 

    byte* _led_state;
    
    void clk(void);
    void sendByte(byte b);
    void sendColor(byte red, byte green, byte blue);
};

#endif

