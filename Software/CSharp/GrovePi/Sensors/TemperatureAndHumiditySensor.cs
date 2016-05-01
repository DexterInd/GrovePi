using System;

namespace GrovePi.Sensors
{
    public interface ITemperatureAndHumiditySensor
    {
        double TemperatureInCelsius();
    }

    /// <summary>
    /// Specifies the model of sensor. 
    /// DHT11 - blue one - comes with the GrovePi+ Starter Kit.
    /// DHT22 - white one, aka DHT Pro or AM2302.
    /// DHT21 - black one, aka AM2301.
    /// </summary>
    public enum Model
    {
        /* 
        */
        Dht11 = 3975,
        Dht21 = 4250,
        Dht22 = 4250
    }

    internal class TemperatureAndHumiditySensor : ITemperatureAndHumiditySensor
    {
        private readonly IGrovePi _device;
        private readonly Model _model;
        private readonly Pin _pin;

        internal TemperatureAndHumiditySensor(IGrovePi device, Pin pin, Model model)
        {
            if (device == null) throw new ArgumentNullException(nameof(device));
            _device = device;
            _pin = pin;
            _model = model;
        }

        public double TemperatureInCelsius()
        {
            var result = (double) _device.AnalogRead(_pin);
            var resistance = (1023 - result)*10000/result;
            return 1/(Math.Log(resistance/10000)/(int) _model + 1/298.15) - 273.15;
        }
    }
}