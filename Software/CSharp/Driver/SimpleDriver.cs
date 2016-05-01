using System;
using System.Threading.Tasks;
using Windows.ApplicationModel.Background;
using GrovePi;
using GrovePi.Sensors;

namespace Driver
{
    public sealed class SimpleDriver : IBackgroundTask
    {
        private readonly IBuildGroveDevices _deviceFactory = DeviceFactory.Build;

        public void Run(IBackgroundTaskInstance taskInstance)
        {
            var led = _deviceFactory.Led(Pin.DigitalPin5);
            var rotaryAngleSensor = _deviceFactory.RotaryAngleSensor(Pin.AnalogPin2);
            var maxValue = 255;
            while (true)
            {
                try
                {
                    var sensorValue = rotaryAngleSensor.SensorValue();
                    led.AnalogWrite((byte)(sensorValue > maxValue ? maxValue : sensorValue));
                    Task.Delay(500).Wait();
                }
                catch (Exception)
                {

                    throw;
                }
            }
        }
    }
}