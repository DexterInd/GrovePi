// LED Demonstration for the GrovePi.

// This example combines the GrovePi and the Grove LED using the Raspberry Pi and GrovePi.
// The three slowly increase the brightness to full, and reset to 0.  
// http://www.dexterindustries.com/shop/grovepi-board/
// http://www.dexterindustries.com/shop/grove-green-led/
// http://www.dexterindustries.com/shop/grove-blue-led/
// http://www.dexterindustries.com/shop/grove-white-led/
// http://www.dexterindustries.com/shop/grove-red-led/

/*
    1. LED Socket Kit (Blue color) to __D5__(Digital Pin 5)
    2. LED Socket Kit (Red color) to __D6__(Digital Pin 6)
    3. LED Socket Kit (White color) to __D7__(Digital Pin 7)
*/

/*
The MIT License(MIT)

GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
Copyright (C) 2016  Dexter Industries

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
*/

using System;
using Windows.ApplicationModel.Background;
using System.Threading.Tasks;

// Add using statements to the GrovePi libraries
using GrovePi;
using GrovePi.Sensors;

namespace LEDTest
{
    public sealed class StartupTask : IBackgroundTask
    {

        public void Run(IBackgroundTaskInstance taskInstance)
        {

            // Digital Pins 5 and 6 are Pulse Width Modulated (PWM)
            ILed red = DeviceFactory.Build.Led(Pin.DigitalPin5);
            ILed blue = DeviceFactory.Build.Led(Pin.DigitalPin6);
            // Digital port 7 will not PWM.  It is purely digital not 
            // Pulse Width Modulated (PWM).  
            ILed white = DeviceFactory.Build.Led(Pin.DigitalPin7);
            // We will cycle brightness in a while loop.  Type is int
            // so we can perform arithmetic on it.  
            int brightness = 0;

            // Loop endlessly
            while (true)
            {
                try
                {
                    System.Diagnostics.Debug.WriteLine("Brightness: " + brightness.ToString());
                    Task.Delay(100).Wait();     // Delay 0.1 second

                    // Check the brightness, if it's going to overflow, reset it.
                    if (brightness > 250)
                    {
                        brightness = 0;
                    }
                    
                    // Increase the brightness by 5 points.
                    brightness = brightness + 5;
                    // Write the values to the three LEDs.
                    // USA!  Red, White, and Blue!
                    red.AnalogWrite(Convert.ToByte(brightness));
                    blue.AnalogWrite(Convert.ToByte(brightness));
                    white.AnalogWrite(Convert.ToByte(brightness));

                }
                
                catch (Exception ex)
                {
                    // NOTE: There are frequent exceptions of the following:
                    // WinRT information: Unexpected number of bytes was transferred. Expected: '. Actual: '.
                    // This appears to be caused by the rapid frequency of writes to the GPIO
                    // These are being swallowed here/

                    // If you want to see the exceptions uncomment the following:
                    // System.Diagnostics.Debug.WriteLine(ex.ToString());
                }
            }
        }
    }
}
