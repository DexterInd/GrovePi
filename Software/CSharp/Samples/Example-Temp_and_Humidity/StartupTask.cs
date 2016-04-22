// DHT (Temperature and Humidity) Sensor Demonstration for the GrovePi.

// This example combines the GrovePi and the Grove Temp And Humid using the Raspberry Pi and GrovePi.  This is the blue
// sensor found in the GrovePi Base Kit.  
// http://www.dexterindustries.com/shop/grovepi-board/
// http://www.dexterindustries.com/shop/grove-SoundSensor/

// Connct the Temperature (DHT) Sensor to Digial Port 4 on the GrovePi.

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

namespace TempAndHumid
{
    public sealed class StartupTask : IBackgroundTask
    {
        public void Run(IBackgroundTaskInstance taskInstance)
        {
            // Connect the Sound Sensor to Digital port 4
            // Models of Temp and Humidity sensors are - Dht11, Dht12, Dht21
            // In this example, we use the DHT11 sensor that comes with the GrovePi Starter Kit.
            /// Specifies the model of sensor. 
            /// DHT11 - blue one - comes with the GrovePi+ Starter Kit.
            /// DHT22 - white one, aka DHT Pro or AM2302.
            /// DHT21 - black one, aka AM2301.
           
            IDHTTemperatureAndHumiditySensor sensor = DeviceFactory.Build.DHTTemperatureAndHumiditySensor(Pin.DigitalPin4, DHTModel.Dht11);

            // Loop endlessly
            while (true)
            {
                Task.Delay(1000).Wait(); //Delay 1 second
                try
                {
                    // Check the value of the Sensor.
                    // Temperature in Celsius is returned as a double type.  Convert it to string so we can print it.
                    sensor.Measure();
                    string sensortemp = sensor.TemperatureInCelsius.ToString();
                    // Same for Humidity.  
                    string sensorhum = sensor.Humidity.ToString();
                    
                    // Print all of the values to the debug window.  
                    System.Diagnostics.Debug.WriteLine("Temp is " + sensortemp + " C.  And the Humidity is " + sensorhum + "%. ");

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
