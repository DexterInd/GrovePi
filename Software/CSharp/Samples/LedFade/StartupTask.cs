// Adjust LED brightness by rotating Potentiometer

// GrovePi + Rotary Angle Sensor (Potentiometer) + LED
// http://www.seeedstudio.com/wiki/Grove_-_Rotary_Angle_Sensor
// http://www.seeedstudio.com/wiki/Grove_-_LED_Socket_Kit

/*
The MIT License(MIT)

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
*/

using System;
using Windows.ApplicationModel.Background;

// Add using statements to the GrovePi libraries
using GrovePi;
using GrovePi.Sensors;

namespace LedFade
{
    public sealed class StartupTask : IBackgroundTask
    {
        public void Run(IBackgroundTaskInstance taskInstance)
        {
            // Connect the Rotary Angle Sensor to analog port 2
            IRotaryAngleSensor potentiometer = DeviceFactory.Build.RotaryAngleSensor(Pin.AnalogPin2);

            // Connect the LED to digital port 5
            ILed led = DeviceFactory.Build.Led(Pin.DigitalPin5);

            // Create a variable to track the LED brightness
            double brightness = 0;

            // Capture the current value from the Rotary Angle sensor
            double angle = 0;

            // Loop endlessly
            while (true)
            {
                try
                {
                    // Capture the current value from the Rotary Angle sensor
                    angle = potentiometer.SensorValue();

                    // Output the agle to the Output Window
                    System.Diagnostics.Debug.WriteLine("Angle is " + angle.ToString());

                    // If the Rotary Angle sensor value is greater than zero...
                    if (angle > 0)
                    {
                        // Divide the angle (a 10-bit value from 0-1023) by four
                        // to get a single byte value value from 0-255.
                        brightness = Math.Floor(angle / 4);
                    }
                    else
                    {
                        // If the angle is zero, set the brightness to zero
                        brightness = 0;
                    }

                    // Output the brightness to the Output Window
                    System.Diagnostics.Debug.WriteLine("Brightness is " + brightness.ToString());

                    // AnalogWrite uses Pulse WIdth Modulation (PWM) to 
                    // control the brightness of the digital LED.
                    led.AnalogWrite(Convert.ToByte(brightness));
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
