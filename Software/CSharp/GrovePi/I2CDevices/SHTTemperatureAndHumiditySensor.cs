using Windows.Devices.I2c;

namespace GrovePi.I2CDevices
{
    /// <summary>
    /// 
    /// </summary>
    public interface ISHTTemperatureAndHumiditySensor
    {
        double TemperatureInCelsius { get; }
        double TemperatureInFahrenheit { get; }
        double RelativeHumidity { get; }
        void Measure();
    }

    /// <summary>
    /// Specifies the model of sensor.
    /// </summary>
    public enum SHTModel
    {
        Sht31 = 0
    }

    /// <summary>
    /// The repeatability setting influences the measurement duration and the current
    /// consumption of the sensor.
    /// </summary>
    public enum MeasurementMode
    {
        HighRepeatClockStretch = 0,
        MediumRepeatClockStretch,
        LowRepeatClockStretch,
        HighRepeat,
        MediumRepeat,
        LowRepeat
    }

    internal class SHTTemperatureAndHumiditySensor : ISHTTemperatureAndHumiditySensor
    {
        private readonly SHTModel _model;
        internal I2cDevice _device;

        private byte[] MeasureHighClockStretch = new byte[2] { 0x2C, 0x06 };
        private byte[] MeasureMediumClockStretch = new byte[2] { 0x2C, 0x0D };
        private byte[] MeasureLowClockStretch = new byte[2] { 0x2C, 0x10 };
        private byte[] MeasureHigh = new byte[2] { 0x24, 0x00 };
        private byte[] MeasureMedium = new byte[2] { 0x24, 0x0B };
        private byte[] MeasureLow = new byte[2] { 0x24, 0x16 };

        private byte[] ReadStatusRegisterCommandAddress = new byte[2] { 0xF3, 0x2D };
        private byte[] ClearStatusRegisterCommandAddress = new byte[2] { 0x30, 0x41 };
        private byte[] SoftResetCommandAddress = new byte[2] { 0x30, 0xA2 };
        private byte[] EnableHeaterCommandAddress = new byte[2] { 0x30, 0x6D };
        private byte[] DisableHeaderCommandAddress = new byte[2] { 0x30, 0x66 };
        private byte[] BreakCommandAddress = new byte[2] { 0x30, 0x93 };

        private byte[] _sensorData = new byte[6];
        private byte[] _sensorCommand = new byte[4];

        public double TemperatureInCelsius { get; set; }
        public double TemperatureInFahrenheit { get; set; }
        public double RelativeHumidity { get; set; }

        internal SHTTemperatureAndHumiditySensor(I2cDevice sensorDevice, SHTModel model, MeasurementMode measureMode)
        {
            _device = sensorDevice;
            _model = model;

            switch (measureMode)
            {
                case MeasurementMode.HighRepeatClockStretch:
                    _sensorCommand = MeasureHighClockStretch;
                    break;
                case MeasurementMode.MediumRepeatClockStretch:
                    _sensorCommand = MeasureMediumClockStretch;
                    break;
                case MeasurementMode.LowRepeatClockStretch:
                    _sensorCommand = MeasureLowClockStretch;
                    break;
                case MeasurementMode.HighRepeat:
                    _sensorCommand = MeasureHigh;
                    break;
                case MeasurementMode.MediumRepeat:
                    _sensorCommand = MeasureMedium;
                    break;
                case MeasurementMode.LowRepeat:
                    _sensorCommand = MeasureLow;
                    break;
                default:
                    _sensorCommand = MeasureHigh;
                    break;
            }
        }

        public void Measure()
        {
            _device.WriteRead(_sensorCommand, _sensorData);

            TemperatureInCelsius = (((_sensorData[0] * 256) + _sensorData[1]) * 175.0) / 65535.0 - 45.0;
            TemperatureInFahrenheit = (((_sensorData[0] * 256) + _sensorData[1]) * 315.0) / 65535.0 - 49.0;
            RelativeHumidity = (((_sensorData[3] * 256) + _sensorData[4])) * 100.0 / 65535.0 - 6.0;
        }

        /// <summary>
        /// This triggers the sensor to reset its system controller and reloads calibration data from the memory.
        /// </summary>
        public void Reset()
        {
            _device.Write(SoftResetCommandAddress);
        }

        /// <summary>
        /// All flags (Bit 15, 11, 10, 4) in the status register can be cleared (set to zero)
        /// </summary>
        public void ClearStatusRegister()
        {
            _device.Write(ClearStatusRegisterCommandAddress);
        }

        /// <summary>
        /// The status register contains information on the operational status of the heater, the alert mode and on
        /// the execution status of the last command and the last write sequence.
        /// </summary>
        /// <returns>16bit status register response</returns>
        public byte[] ReadStatusRegister()
        {
            var statusResponse = new byte[2];
            _device.WriteReadPartial(ReadStatusRegisterCommandAddress, statusResponse);
            return statusResponse;
        }

        /// <summary>
        /// The heater can be switched on and off by command
        /// </summary>
        public void EnableHeater()
        {
            _device.Write(EnableHeaterCommandAddress);
        }

        public void DisableHeater()
        {
            _device.Write(DisableHeaderCommandAddress);
        }

        /// <summary>
        /// It is rrecommended to stop the periodic data acquisition prior to sending another command using the break command.
        /// Upon reception of the break command the sensor enters the single shot mode.
        /// </summary>
        internal void Break()
        {
            _device.Write(BreakCommandAddress);
        }

    }
}