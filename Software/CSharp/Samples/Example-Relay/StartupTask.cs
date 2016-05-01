// Relay Demonstration for the GrovePi.

// This example combines the GrovePi and the Grove Relay using the Raspberry Pi and GrovePi.
// http://www.dexterindustries.com/shop/grovepi-board/
// http://www.dexterindustries.com/shop/grove-Relay/

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


namespace Relay
{
    public sealed class StartupTask : IBackgroundTask
    {
        public void Run(IBackgroundTaskInstance taskInstance)
        {
            // Connect the Relay to Digital Pin 5
            // Initialize the relay on Digital Pin 5 (D5)
            IRelay relay = DeviceFactory.Build.Relay(Pin.DigitalPin5);
            
            // Loop endlessly
            while (true)
            {
                try
                {
                    // Turn the Relay On.
                    relay.ChangeState(SensorStatus.On);                     // Turn the relay on.
                    System.Diagnostics.Debug.WriteLine("Button is On.");    // Write something to debug.
                    Task.Delay(1000).Wait();                                // Delay 1 second

                    // Turn the Relay Off.
                    relay.ChangeState(SensorStatus.Off);                    // Turn the relay off.
                    System.Diagnostics.Debug.WriteLine("Button is Off.");   // Write this fact to debug.
                    Task.Delay(1000).Wait();                                // Delay 1 second     
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
