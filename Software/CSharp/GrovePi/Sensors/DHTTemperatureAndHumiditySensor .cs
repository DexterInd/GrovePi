using System;
using GrovePi.Common;

namespace GrovePi.Sensors
{
    public interface IDHTTemperatureAndHumiditySensor
    {
        double TemperatureInCelsius();
        double TemperatureInFahrenheit();
        double Humidity();
    }

    /// <summary>
    /// Specifies the model of sensor. 
    /// DHT11 - blue one - comes with the GrovePi+ Starter Kit.
    /// DHT22 - white one, aka DHT Pro or AM2302.
    /// DHT21 - black one, aka AM2301.
    /// </summary>
    public enum DHTModel
    {
        /* 
        */
        Dht11 = 0,
        Dht21 = 1,
        Dht22 = 2
    }

    internal class DHTTemperatureAndHumiditySensor : IDHTTemperatureAndHumiditySensor
    {
        private readonly GrovePi _device;
        private readonly DHTModel _model;
        private readonly Pin _pin;

        private const byte DHTCmd = 40;

        internal DHTTemperatureAndHumiditySensor(GrovePi device, Pin pin, DHTModel model)
        {
            if (device == null) throw new ArgumentNullException(nameof(device));
            _device = device;
            _pin = pin;
            _model = model;
        }

        public double TemperatureInCelsius()
        {
            _device.DirectAccess.Write(new byte[] { DHTCmd, (byte)_pin, (byte)_model, 0 });
            Delay.Milliseconds(600);

            var readBuffer = new byte[9];
            _device.DirectAccess.Read(readBuffer);

            float tmp = BitConverter.ToSingle(readBuffer, 1);

            return (double)tmp;
        }

        private double CtoF(double c)
        {
            return c * 9 / 5 + 32;
        }

        public double TemperatureInFahrenheit()
        {
            return CtoF(TemperatureInCelsius());
        }

        public double Humidity()
        {
            _device.DirectAccess.Write(new byte[] { DHTCmd, (byte)_pin, (byte)_model, 0 });
            Delay.Milliseconds(600);

            var readBuffer = new byte[9];
            _device.DirectAccess.Read(readBuffer);

            float tmp = BitConverter.ToSingle(readBuffer, 5);

            return (double)tmp;
        }
    }
}