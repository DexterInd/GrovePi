using System;
using Windows.ApplicationModel.Background;

// Add using statements to the GrovePi libraries
using GrovePi;
using GrovePi.Sensors;

namespace GasSensorMQ2
{
    public sealed class StartupTask : IBackgroundTask
    {
        public void Run(IBackgroundTaskInstance taskInstance)
        {
            // Connect the Gas Sensor MQ2 to analog port 0
            IGasSensorMQ2 sensor = DeviceFactory.Build.GasSensorMQ2(Pin.AnalogPin0);

            // Loop endlessly
            while (true)
            {
                try
                {
                    // Check the value of the button, turn it into a string.
                    string sensorvalue = sensor.SensorValue().ToString();
                    System.Diagnostics.Debug.WriteLine("Gas Sensor value is " + sensorvalue);

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

