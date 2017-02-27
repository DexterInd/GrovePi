// Grove OLED Display 96*96 demo

// GrovePi + Grove OLED Display 96*96
// https://www.seeedstudio.com/Grove-OLED-Display-1.12%22-p-824.html

/*
The MIT License(MIT)

GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
Copyright (C) 2015  Dexter Industries

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

using Windows.System.Threading;
using GrovePi;
using GrovePi.Sensors;
using GrovePi.I2CDevices;
using System.Diagnostics;

using Windows.ApplicationModel.Background;

// The Background Application template is documented at http://go.microsoft.com/fwlink/?LinkID=533884&clcid=0x409

namespace OLEDDisplay9696
{
    public sealed class StartupTask : IBackgroundTask
    {
        BackgroundTaskDeferral deferral;
        ThreadPoolTimer timer;
        IOLEDDisplay9696 oled;
        DateTime now;
        private const string content = "Grove OLED!";

        public void Run(IBackgroundTaskInstance taskInstance)
        {
            deferral = taskInstance.GetDeferral();
            oled = DeviceFactory.Build.OLEDDisplay9696();
            oled.initialize();
            oled.clearDisplay();
            oled.setNormalDisplay();
            oled.setVerticalMode();
            oled.setGrayLevel(15);
            oled.setTextXY(0, 0);
            oled.putString(content);

            timer = ThreadPoolTimer.CreatePeriodicTimer(this.Timer_Tick, TimeSpan.FromSeconds(1));
        }

        private void Timer_Tick(ThreadPoolTimer timer)
        {
            try
            {
                now = DateTime.Now;
                oled.setTextXY(4, 0);
                oled.putString(now.ToString("yyyy-MM-dd"));
                oled.setTextXY(6, 0);
                oled.putString(now.ToString("HH:mm:ss tt"));
                Debug.WriteLine("Debug - " + now);
            }
            catch (Exception ex)
            {
            }
        }
    }
}
