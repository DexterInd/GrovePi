using System;

namespace GrovePi.Sensors
{
    public interface IGasSensorMQ2
    {
        int SensorValue();
    }

    internal class GasSensorMQ2 : Sensor<IGasSensorMQ2>, IGasSensorMQ2
    {
        public GasSensorMQ2(GrovePi device, Pin pin) : base(device,pin,PinMode.Input)
        {

        }

        public int SensorValue()
        {
            return Device.AnalogRead(Pin);
        }
    }
}
