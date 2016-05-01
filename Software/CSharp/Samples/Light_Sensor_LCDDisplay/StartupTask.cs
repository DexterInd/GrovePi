// Use the RGB Display and the Light Sensor
// In this example, we print the value of the light sensor on the RGB Display
// and change the color of the RGB display based on the value of the light sensor. 


// The GrovePi connects the Raspberry Pi and Grove sensors.  
// You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi

// This example combines the GrovePi + Light Sensor + RGB Display
// http://www.dexterindustries.com/shop/grovepi-board/
// http://www.seeedstudio.com/depot/Grove-LCD-RGB-Backlight-p-1643.html
// http://www.dexterindustries.com/shop/grove-light-sensor/

// Hardware Setup:
// Connect the Light Sensor to Analog Port 1.
// Connect the RGB Display to any I2C Port.

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
using System.Text;
using Windows.ApplicationModel.Background;
using System.Threading.Tasks;

// Add using statements to the GrovePi libraries
using GrovePi;
using GrovePi.Sensors;
using GrovePi.I2CDevices;

namespace LightSensorLCDDisplay
{
    public sealed class StartupTask : IBackgroundTask
    {
        public void Run(IBackgroundTaskInstance taskInstance)
        {
            System.Diagnostics.Debug.WriteLine("Starting program!");
        
            // The RGB display is an I2C device and can be connected to any one of the I2C ports.
            IRgbLcdDisplay rgbdisplay = DeviceFactory.Build.RgbLcdDisplay();

            // Connect the Light Sensor to analog port 1
            IRotaryAngleSensor lightsensor = DeviceFactory.Build.RotaryAngleSensor(Pin.AnalogPin1);
            double brightness = 0;

            // Loop endlessly
            while (true)
            {
                try
                {
                    // Check the value of the button.
                    brightness = lightsensor.SensorValue();

                    // Print out Brightness to Debug.
                    System.Diagnostics.Debug.WriteLine("Raw Brightness is: " + brightness.ToString());

                    // Typecase the double to byte for the automatic brightness function!
                    byte brightbyte = (byte)brightness; // The SetBacklightRgb function takes a byte type.
                    // Set the display based on the light levels.
                    rgbdisplay.SetBacklightRgb(brightbyte, brightbyte, brightbyte);

                    // Use a StringBuilder to assemble the display text
                    StringBuilder lightstring = new StringBuilder();

                    // Print the value of the light sensor to the LCD Screen.
                    lightstring.Append(brightness.ToString());
                    System.Diagnostics.Debug.WriteLine("Display: " + lightstring.ToString());
                    rgbdisplay.SetText(lightstring.ToString());
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

                // Delay in here to allow you to read the light sensor value.  
                // If you don't include a short delay, the LCD screen will appear to be blank!
                Task.Delay(500).Wait(); //Delay 1 second
            }
        }
    }
}
