using System;

namespace GrovePi.Sensors
{
    public interface ITemperatureSensor
    {
        double TemperatureInCelsius();
    }

    /// <summary>
    /// Temperature Sensor V1.1 & 1.2
    /// ref: <http://wiki.seeed.cc/Grove-Temperature_Sensor_V1.2/>
    /// </summary>
    internal class TemperatureSensor : ITemperatureSensor
    {
        private readonly IGrovePi _device;
        private readonly Pin _pin;

        internal TemperatureSensor(IGrovePi device, Pin pin)
        {
            if (device == null) throw new ArgumentNullException(nameof(device));
            _device = device;
            _pin = pin;
        }

        public double TemperatureInCelsius()
        {
            var result = (double)_device.AnalogRead(_pin);
            var resistance = (1023 - result) * 10000 / result;
            return 1 / (Math.Log(resistance / 10000) / 4275 + 1 / 298.15) - 273.15;
        }
    }
}
