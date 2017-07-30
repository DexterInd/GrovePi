// Sample of Grove Mini Motor Drive, make two channel output a stable pwm

// Grove Pi + Grove Mini Motor Driver
// https://www.seeedstudio.com/Grove%C2%A0%C2%A0I2C%C2%A0Mini%C2%A0Motor%C2%A0Driver-p-2508.html?cPath=91_92

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
using Windows.ApplicationModel.Background;

using Windows.System.Threading;
using GrovePi;
using GrovePi.I2CDevices;
using System.Diagnostics;

// The Background Application template is documented at http://go.microsoft.com/fwlink/?LinkID=533884&clcid=0x409

namespace MiniMotorDriver
{
    public sealed class StartupTask : IBackgroundTask
    {
        // MiniMotorDriver.drive(Speed), limited Speed at -63 ~ 63, 
        // use positive number to drive ahead and negative number to drive back. 
        // Input zero to stop 
        BackgroundTaskDeferral deferral;
        IMiniMotorDriver motor;
        ThreadPoolTimer timer;
        volatile int speed = 0;
        volatile bool direction = false;


        public void Run(IBackgroundTaskInstance taskInstance)
        {
            deferral = taskInstance.GetDeferral();

            motor = DeviceFactory.Build.MiniMotorDriver(0xD0, 0xC0);
            timer = ThreadPoolTimer.CreatePeriodicTimer(new TimerElapsedHandler(Timer_tick), TimeSpan.FromSeconds(.2));

        }

        private void Timer_tick(ThreadPoolTimer timer)
        {
            try
            {
                if (direction)
                {
                    speed += 1;
                }
                else
                {
                    speed -= 1;
                }

                if (speed > 40)
                {
                    direction = false;
                }
                if (speed < -40)
                {
                    direction = true;
                }
                motor.drive1(speed);
                motor.drive2(-speed);
            }
            catch (Exception ex)
            {
                Debug.WriteLine(ex);
            }
        }
    }
}
