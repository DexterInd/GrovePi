﻿// Grove OLED Display 96*96 demo

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
using GrovePi.Common;

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

        byte [] SeeedLogo = 
        {

        0x00, 0x00, 0x00, 0x00, 0x00, 0x20, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x60, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xC0, 0x06, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0xC0, 0x07, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x01, 0xC0, 0x07, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x03, 0x80, 0x03, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03, 0x80, 0x03, 0x80,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x07, 0x80, 0x03, 0xC0, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x07, 0x80, 0x01, 0xC0, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x20,
        0x07, 0x80, 0x01, 0xE0, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x20, 0x0F, 0x80, 0x01, 0xE0,
        0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x30, 0x0F, 0x00, 0x01, 0xE0, 0x08, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x30, 0x0F, 0x00, 0x01, 0xE0, 0x18, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x30,
        0x0F, 0x00, 0x01, 0xE0, 0x18, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x30, 0x0F, 0x00, 0x01, 0xE0,
        0x18, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x38, 0x0F, 0x00, 0x01, 0xE0, 0x18, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x38, 0x0F, 0x00, 0x01, 0xE0, 0x38, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x38,
        0x0F, 0x80, 0x01, 0xE0, 0x38, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x3C, 0x0F, 0x80, 0x01, 0xE0,
        0x78, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x3E, 0x0F, 0x80, 0x03, 0xE0, 0x78, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x1E, 0x07, 0x80, 0x03, 0xE0, 0xF8, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1E,
        0x07, 0x80, 0x03, 0xE0, 0xF0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1F, 0x07, 0x80, 0x03, 0xC1,
        0xF0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0F, 0x87, 0xC0, 0x07, 0xC1, 0xF0, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x0F, 0x83, 0xC0, 0x07, 0x83, 0xE0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0F,
        0xC3, 0xC0, 0x07, 0x87, 0xE0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x07, 0xE1, 0xE0, 0x07, 0x0F,
        0xC0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03, 0xF0, 0xE0, 0x0F, 0x0F, 0x80, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x01, 0xF8, 0xF0, 0x0E, 0x1F, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01,
        0xF8, 0x70, 0x1C, 0x3F, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFC, 0x30, 0x18, 0x7E,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x7F, 0x18, 0x30, 0xFC, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x1F, 0x88, 0x21, 0xF0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x0F, 0xC4, 0x47, 0xE0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03, 0xE0, 0x0F, 0x80,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xF8, 0x3E, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x0E, 0xE0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x6C, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x02, 0x00, 0x06, 0x00, 0x00, 0x6C, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x00, 0x06,
        0x00, 0x00, 0x60, 0x00, 0x7E, 0x3F, 0x0F, 0xC3, 0xF0, 0xFA, 0x0F, 0xDF, 0xE1, 0x9F, 0xEC, 0x7E,
        0xE6, 0x73, 0x9C, 0xE7, 0x39, 0xCE, 0x1C, 0xDF, 0xE1, 0xB9, 0xEC, 0xE7, 0xE0, 0x61, 0xD8, 0x66,
        0x1B, 0x86, 0x1C, 0x06, 0x61, 0xB0, 0x6D, 0xC3, 0x7C, 0x7F, 0xFF, 0xFF, 0xFF, 0x06, 0x0F, 0x86,
        0x61, 0xB0, 0x6D, 0x83, 0x3E, 0x7F, 0xFF, 0xFF, 0xFF, 0x06, 0x07, 0xC6, 0x61, 0xB0, 0x6D, 0x83,
        0xC3, 0x61, 0x18, 0x46, 0x03, 0x86, 0x18, 0x66, 0x61, 0xB0, 0x6D, 0xC3, 0xFE, 0x7F, 0x9F, 0xE7,
        0xF9, 0xFE, 0x1F, 0xE6, 0x3F, 0x9F, 0xEC, 0xFE, 0x7E, 0x3F, 0x0F, 0xC3, 0xF0, 0xFA, 0x0F, 0xC6,
        0x3F, 0x9F, 0xEC, 0x7E, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x7C, 0x00,
        0x00, 0x20, 0x82, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x44, 0x00, 0x00, 0x20, 0x82, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x6C, 0xF3, 0xCF, 0x70, 0x9E, 0x79, 0xE7, 0x80, 0x00, 0x00,
        0x00, 0x00, 0x7D, 0x9E, 0x68, 0x20, 0xB2, 0xC8, 0x64, 0x00, 0x00, 0x00, 0x00, 0x00, 0x47, 0x9E,
        0x6F, 0x20, 0xB2, 0xF9, 0xE7, 0x80, 0x00, 0x00, 0x00, 0x00, 0x46, 0x9A, 0x61, 0x20, 0xB2, 0xCB,
        0x60, 0x80, 0x00, 0x00, 0x00, 0x00, 0x7C, 0xF3, 0xCF, 0x30, 0x9E, 0x79, 0xE7, 0x90, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x7C, 0x02, 0x00, 0x00, 0x82, 0x60, 0x00, 0x00,
        0xF8, 0x00, 0x00, 0x40, 0x40, 0x02, 0x00, 0x00, 0x83, 0x60, 0x00, 0x00, 0x8C, 0x00, 0x00, 0x40,
        0x60, 0xB7, 0x79, 0xE7, 0x81, 0xC7, 0x92, 0x70, 0x89, 0xE7, 0x9E, 0x78, 0x7C, 0xE2, 0xC9, 0x2C,
        0x81, 0xCC, 0xD2, 0x40, 0xFB, 0x21, 0xB2, 0x48, 0x40, 0x62, 0xF9, 0x2C, 0x80, 0x8C, 0xD2, 0x40,
        0x8B, 0xE7, 0xB0, 0x48, 0x40, 0xE2, 0xC9, 0x2C, 0x80, 0x84, 0xD2, 0x40, 0x8B, 0x2D, 0x92, 0x48,
        0x7D, 0xB3, 0x79, 0x27, 0x80, 0x87, 0x9E, 0x40, 0x8D, 0xE7, 0x9E, 0x48, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
        };

        public void Run(IBackgroundTaskInstance taskInstance)
        {
            deferral = taskInstance.GetDeferral();
            oled = DeviceFactory.Build.OLEDDisplay9696();
            oled.initialize();
            oled.clearDisplay();
            oled.drawBitmap(SeeedLogo, 96 * 96 / 8);
            oled.setNormalDisplay();
            oled.setVerticalMode();
            oled.setGrayLevel(15);
            Delay.Milliseconds(2000);
            oled.setTextXY(5, 0);
            oled.putString("            ");
            oled.setTextXY(6, 0);
            oled.putString("            ");
            timer = ThreadPoolTimer.CreatePeriodicTimer(this.Timer_Tick, TimeSpan.FromSeconds(1));
        }

        private void Timer_Tick(ThreadPoolTimer timer)
        {
            try
            {
                now = DateTime.Now;
                oled.setTextXY(5, 0);
                oled.putString(now.ToString("yyyy-MM-dd  "));
                oled.setTextXY(7, 0);
                oled.putString(now.ToString("HH:mm:ss tt "));
                Debug.WriteLine("Debug - " + now);
            }
            catch (Exception ex)
            {
            }
        }
    }
}
