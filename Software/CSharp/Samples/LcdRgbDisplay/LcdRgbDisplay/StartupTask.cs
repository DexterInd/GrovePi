// Display text and change background color on the LCD RGB Backlight Display

// GrovePi + LCD RGB Backlight Display
// http://www.seeedstudio.com/wiki/Grove_-_LCD_RGB_Backlight

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
using System.Text;
using Windows.ApplicationModel.Background;

using Windows.System.Threading;
using GrovePi;
using GrovePi.I2CDevices;

namespace LcdRgbDisplay
{
    public sealed class StartupTask : IBackgroundTask
    {
        ThreadPoolTimer timer;
        BackgroundTaskDeferral deferral;
        IRgbLcdDisplay display;
        DateTime now;
        string ampm;


        public void Run(IBackgroundTaskInstance taskInstance)
        {
            deferral = taskInstance.GetDeferral();

            // Connect the RGB display to one of the I2C ports
            display = DeviceFactory.Build.RgbLcdDisplay();

            // Create a timer that will 'tick' every half-second (500ms)
            timer = ThreadPoolTimer.CreatePeriodicTimer(this.Timer_Tick, TimeSpan.FromSeconds(1));
        }

        private void Timer_Tick(ThreadPoolTimer timer)
        {
            try
            {
                // Get the current time
                now = DateTime.Now;

                // Use a StringBuilder to assemble the display text
                StringBuilder timeString = new StringBuilder();

                if (now.Hour > 12)
                {
                    // Set the RGB backlight to a light blue-ish color
                    display.SetBacklightRgb(0, 255, 255);

                    timeString.Append("Good evening.\n");
                    ampm = " PM";
                    timeString.Append(now.Hour - 12);
                }
                else
                {
                    // Set the RGB backlight to a light yellow-ish color
                    display.SetBacklightRgb(255, 255, 0);

                    timeString.Append("Good morning.\n");
                    ampm = " AM";
                    timeString.Append(now.Hour);
                }

                timeString.Append(":");
                timeString.Append(now.Minute.ToString("D2"));
                timeString.Append(":");
                timeString.Append(now.Second.ToString("D2"));
                timeString.Append(ampm);

                // Display the time
                display.SetText(timeString.ToString());
            }
            catch (Exception ex)
            {

            }
        }
    }
}
