using System;
using Windows.ApplicationModel.Background;
using System.Threading.Tasks;

// Add using statements to the GrovePi libraries
using GrovePi;
using GrovePi.Sensors;

namespace PIRMotionSensor
{
    public sealed class StartupTask : IBackgroundTask
    {
        public void Run(IBackgroundTaskInstance taskInstance)
        {
            // Connect the Sound Sensor to digital port 5
            IPIRMotionSensor pirMotion = DeviceFactory.Build.PIRMotionSensor(Pin.DigitalPin5);

            // Loop endlessly
            while (true)
            {
                try
                {
                    // Check people motion
                    if (pirMotion.IsPeopleDetected())
                    {
                        System.Diagnostics.Debug.WriteLine("Have people motion");
                    }
                    Task.Delay(1000).Wait();
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
