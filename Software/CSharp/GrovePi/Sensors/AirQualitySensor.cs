using System;


namespace GrovePi.Sensors
{
    public interface IAirQualitySensor
    {
        int AirQuality();
    }
    internal class AirQualitySensor : IAirQualitySensor
    {
        private readonly GrovePi _device;
        private readonly Pin _pin;

        internal AirQualitySensor(GrovePi device, Pin pin)
        {
            if (device == null) throw new ArgumentNullException(nameof(device));
            device.PinMode(_pin, PinMode.Input);
            _device = device;
            _pin = pin;
        }
        public int AirQuality()
        {
            return _device.AnalogRead(_pin);
        }
    }
}
