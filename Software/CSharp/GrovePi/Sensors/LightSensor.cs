using System;

namespace GrovePi.Sensors
{
    public interface ILightSensor
    {
        int SensorValue();
        double Resistance();
    }

    internal class LightSensor : ILightSensor
    {
        private readonly GrovePi _device;
        private readonly Pin _pin;

        internal LightSensor(GrovePi device, Pin pin)
        {
            if (device == null) throw new ArgumentNullException(nameof(device));
            device.PinMode(_pin, PinMode.Input);
            _device = device;
            _pin = pin;
        }

        public int SensorValue()
        {
            return _device.AnalogRead(_pin);
        }

        public double Resistance()
        {
            var sensorValue = SensorValue();
            return (double) (1023 - sensorValue)*10/sensorValue;
        }
    }
}
