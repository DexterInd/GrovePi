using System;

namespace GrovePi.Sensors
{
    public interface IRotaryAngleSensor
    {
        int SensorValue();
        double Voltage();
        double Degrees();
    }

    public class RotaryAngleSensor : IRotaryAngleSensor
    {
        private const int FullAngle = 300;
        private readonly GrovePi _device;
        private readonly Pin _pin;

        internal RotaryAngleSensor(GrovePi device, Pin pin)
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

        public double Voltage()
        {
            return Math.Round(((float) SensorValue()*Constants.AdcVoltage/1023), 2);
        }

        public double Degrees()
        {
            return Math.Round((Voltage()*FullAngle)/Constants.GroveVcc, 2);
        }

        public int Brightness()
        {
            return (int) (Degrees()/FullAngle*255);
        }
    }
}