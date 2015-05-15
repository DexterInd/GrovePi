using Windows.ApplicationModel.Background;
using GrovePi;
using GrovePi.Sensors;

namespace Driver
{
    /// <summary>
    /// Library Authors:
    /// John https://github.com/robsonj
    /// Paul Binder Jr https://github.com/Exadon http://www.PaulBinderJr.com
    /// </summary>
    public sealed class SimpleDriver : IBackgroundTask
    {
        private readonly IBuildGroveDevices _deviceFactory = DeviceFactory.Build;

        public void Run(IBackgroundTaskInstance taskInstance)
        {
            //**Samples using the device factor. Un comment as needed**

            //var distance = _deviceFactory
            //    .BuildUltraSonicSensor(Pin.DigitalPin2)
            //    .MeasureInCentimeters();

            //_deviceFactory.BuildBuzzer(Pin.DigitalPin2).ChangeState(SensorStatus.On);

            //        var tempInCelcius = _deviceFactory
            //.BuildTemperatureAndHumiditySensor(Pin.DigitalPin2, Model.OnePointTwo)
            //.TemperatureInCelcius();

            //var level = _deviceFactory.BuildLightSensor(Pin.DigitalPin3)
            //    .SensorValue();
            //_deviceFactory
            //    .BuildBuzzer(Pin.DigitalPin4)
            //    .ChangeState(SensorStatus.On)
            //    .ChangeState(SensorStatus.Off);
        }
    }
}