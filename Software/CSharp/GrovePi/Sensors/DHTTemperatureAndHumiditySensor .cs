using System;
using GrovePi.Common;

namespace GrovePi.Sensors
{
    public interface IDHTTemperatureAndHumiditySensor
    {
        double TemperatureInCelsius { get; }
        double TemperatureInFahrenheit { get; }
        double Humidity { get; }
        void Measure();
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

        private double t = 0;
        private double h = 0;

        internal DHTTemperatureAndHumiditySensor(GrovePi device, Pin pin, DHTModel model)
        {
            if (device == null) throw new ArgumentNullException(nameof(device));
            _device = device;
            _pin = pin;
            _model = model;
        }

        public void Measure()
        {
            _device.DirectAccess.WritePartial(new byte[4] { DHTCmd, (byte)_pin, (byte)_model, Constants.Unused });
            Delay.Milliseconds(600);

            var readBuffer = new byte[9];
            _device.DirectAccess.ReadPartial(readBuffer);

            float t0 = BitConverter.ToSingle(readBuffer, 1);
            float h0 = BitConverter.ToSingle(readBuffer, 5);

            t = (double)t0;
            h = (double)h0;
        }

        private double CtoF(double c)
        {
            return c * 9 / 5 + 32;
        }

        public double TemperatureInCelsius
        {
            get
            {
                return t;
            }
        }

        public double TemperatureInFahrenheit
        {
            get
            {
                return CtoF(t);
            }
        }

        public double Humidity
        {
            get
            {
                return h;
            }
        }
    }
}