// Hello World!  Your first WinIOT project with the GrovePi!
/*

This example simply turns and LED on and off at 1 second intervals.  

The GrovePi connects the Raspberry Pi and Grove sensors.  
You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi

This example combines the GrovePi + LED:
    http://www.dexterindustries.com/shop/grovepi-board/
    http://www.dexterindustries.com/shop/grove-green-led/

Hardware Setup:
    Connect the LED to digital port 2

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
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Net.Http;
using Windows.ApplicationModel.Background;
using System.Threading.Tasks;

// GrovePi Libraries Needed
using GrovePi;
using GrovePi.Sensors;
using Windows.System.Threading;

namespace HelloWorldBlinky
{
    public sealed class StartupTask : IBackgroundTask
    {
        // Create the LED.
        ILed led;
        public async void Run(IBackgroundTaskInstance taskInstance)
        {
            // Initiate the LED on Digital Pin 2.  (D2).
            led = DeviceFactory.Build.Led(Pin.DigitalPin2);

            while (true)
            {
                
                Task.Delay(1000).Wait(); //Delay 1 second
                try
                {
                    // If the LED is on, turn it off.  If the LED is off, turn it on.  
                    led.ChangeState((led.CurrentState == SensorStatus.Off) ? SensorStatus.On : SensorStatus.Off);
                }
                catch (Exception ex)
                {
                    // Do Nothing if there's an exception.
                }
            }
        }
    }
}
