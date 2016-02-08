using System;
using System.Linq;
using GrovePi.I2CDevices.Configuration;
using Windows.Devices.I2c;
using static System.Math;

namespace GrovePi.I2CDevices
{
    public interface ISixAxisAccelerometerAndCompass
    {
        byte DeviceId();

        double[] GetAcceleration();

        double[] GetMagnetic();

        double GetHeading();

        double GetTiltHeading();

        ISixAxisAccelerometerAndCompass Configure(Action<ISixAxisAccelerometerAndCompassConfiguration> configuration);
    }

    public interface ISixAxisAccelerometerAndCompassConfiguration
    {
        void AccelerationAxes(AccelerationAxes value);

        void AccelerationDataRate(AccelerationDataRate value);

        void AccelerationDataUpdateMode(AccelerationDataUpdateMode value);

        void AccelerationScale(AccelerationScale value);

        void MagneticDataRate(MagneticDataRate value);

        void MagneticMode(MagneticMode value);

        void MagneticResolution(MagneticResolution value);

        void MagneticScale(MagneticScale value);
    }

    internal sealed class SixAxisAccelerometerAndCompass : ISixAxisAccelerometerAndCompass
    {
        private const int X = 0;
        private const int Y = 1;
        private const int Z = 2;

        private const double Pow_2_15 = 32768;

        private const byte WHO_AM_I = 0x0f;

        private const byte CTRL_REG0 = 0x1F;
        private const byte CTRL_REG1 = 0x20;
        private const byte CTRL_REG2 = 0x21;
        private const byte CTRL_REG3 = 0x22;
        private const byte CTRL_REG4 = 0x23;
        private const byte CTRL_REG5 = 0x24;
        private const byte CTRL_REG6 = 0x25;
        private const byte CTRL_REG7 = 0x26;

        private const byte OUT_X_L_M = 0x08;
        private const byte OUT_X_H_M = 0x09;
        private const byte OUT_Y_L_M = 0x0A;
        private const byte OUT_Y_H_M = 0x0B;
        private const byte OUT_Z_L_M = 0x0C;
        private const byte OUT_Z_H_M = 0x0D;

        private const byte OUT_X_L_A = 0x28;
        private const byte OUT_X_H_A = 0x29;
        private const byte OUT_Y_L_A = 0x2A;
        private const byte OUT_Y_H_A = 0x2B;
        private const byte OUT_Z_L_A = 0x2C;
        private const byte OUT_Z_H_A = 0x2D;

        internal I2cDevice DirectAccess
        {
            get;
        }

        internal AccelerationAxes AccelerationAxes
        {
            get;
            set;
        } = AccelerationAxes.XYZ;

        internal AccelerationDataRate AccelerationDataRate
        {
            get;
            set;
        } = AccelerationDataRate.Hz_50;

        internal AccelerationDataUpdateMode AccelerationDataUpdateMode
        {
            get;
            set;
        } = AccelerationDataUpdateMode.Continuous;

        internal AccelerationScale AccelerationScale
        {
            get
            {
                return accelerationScale;
            }
            set
            {
                accelerationScale = value;

                switch (accelerationScale)
                {
                    case AccelerationScale.G_2:
                        accelerationScaleFactor = 2.0;
                        break;

                    case AccelerationScale.G_4:
                        accelerationScaleFactor = 4.0;
                        break;

                    case AccelerationScale.G_6:
                        accelerationScaleFactor = 6.0;
                        break;

                    case AccelerationScale.G_8:
                        accelerationScaleFactor = 8.0;
                        break;

                    case AccelerationScale.G_16:
                        accelerationScaleFactor = 16.0;
                        break;
                }
            }
        }

        private AccelerationScale accelerationScale = AccelerationScale.G_2;
        private double accelerationScaleFactor = 2.0;

        internal MagneticDataRate MagneticDataRate
        {
            get;
            set;
        } = MagneticDataRate.Hz_50;

        internal MagneticMode MagneticMode
        {
            get;
            set;
        } = MagneticMode.ContinousConversion;

        internal MagneticResolution MagneticResolution
        {
            get;
            set;
        } = MagneticResolution.Low;

        internal MagneticScale MagneticScale
        {
            get;
            set;
        } = MagneticScale.Gs_4;

        internal SixAxisAccelerometerAndCompass(I2cDevice device)
        {
            if (device == null)
                throw new ArgumentNullException(nameof(device));

            DirectAccess = device;

            Reconfigure();
        }

        public byte DeviceId() => ReadRegister(WHO_AM_I);

        public double[] GetAcceleration()
        {
            // Windows is little-endian so read registers from low to high
            var input = new[]
            {
                ReadRegister(OUT_X_L_A), ReadRegister(OUT_X_H_A),
                ReadRegister(OUT_Y_L_A), ReadRegister(OUT_Y_H_A),
                ReadRegister(OUT_Z_L_A), ReadRegister(OUT_Z_H_A)
            };

            // calculate two's complement value and scale by acceleration factor
            var output = new[]
            {
                BitConverter.ToInt16(input, 0) / Pow_2_15 * accelerationScaleFactor,
                BitConverter.ToInt16(input, 2) / Pow_2_15 * accelerationScaleFactor,
                BitConverter.ToInt16(input, 4) / Pow_2_15 * accelerationScaleFactor
            };

            return output;
        }

        public double[] GetMagnetic()
        {
            // Windows is little-endian so read registers from low to high
            var input = new[]
            {
                ReadRegister(OUT_X_L_M), ReadRegister(OUT_X_H_M),
                ReadRegister(OUT_Y_L_M), ReadRegister(OUT_Y_H_M),
                ReadRegister(OUT_Z_L_M), ReadRegister(OUT_Z_H_M)
            };

            // calculate two's complement value
            var output = new[]
            {
                BitConverter.ToInt16(input, 0) / Pow_2_15,
                BitConverter.ToInt16(input, 2) / Pow_2_15,
                BitConverter.ToInt16(input, 4) / Pow_2_15
            };

            return output;
        }

        public double GetHeading()
        {
            var magnetic = GetMagnetic();

            var heading = 180 * Atan2(magnetic[Y], magnetic[X]) / PI;

            return (heading < 0) ? (heading + 360) : heading;
        }

        public double GetTiltHeading()
        {
            var acceleration = GetAcceleration();

            var pitch = Asin(-acceleration[X]);
            var roll = Asin(acceleration[Y] / Cos(pitch));

            var magnetic = GetMagnetic();

            var xh = magnetic[X] * Cos(pitch) + magnetic[Z] * Sin(pitch);
            var yh = magnetic[X] * Sin(roll) * Sin(pitch) + magnetic[Y] * Cos(roll) - magnetic[Z] * Sin(roll) * Cos(pitch);

            var heading = 180 * Atan2(yh, xh) / PI;

            return (heading < 0) ? (heading + 360) : heading;
        }

        public ISixAxisAccelerometerAndCompass Configure(Action<ISixAxisAccelerometerAndCompassConfiguration> configuration)
        {
            if (configuration != null)
            {
                configuration(new SixAxisAccelerometerAndCompassConfiguration(this));
                Reconfigure();
            }

            return this;
        }

        private byte ReadRegister(byte register)
        {
            var buffer = new byte[1];

            DirectAccess.WriteRead(new[] { register }, buffer);

            return buffer[0];
        }

        private void Reconfigure()
        {
            DirectAccess.Write(new[] { CTRL_REG0, (byte)0 });  // normal mode, FIFO disabled, high-pass filter disabled

            DirectAccess.Write(new[] { CTRL_REG1, (byte)((byte)AccelerationDataRate | (byte)AccelerationDataUpdateMode | (byte)AccelerationAxes) });
            DirectAccess.Write(new[] { CTRL_REG2, (byte)AccelerationScale });

            DirectAccess.Write(new[] { CTRL_REG3, (byte)0 }); // interrupt 1 disabled
            DirectAccess.Write(new[] { CTRL_REG4, (byte)0 }); // interrupt 2 disabled

            DirectAccess.Write(new[] { CTRL_REG5, (byte)((byte)MagneticResolution | (byte)MagneticDataRate) });
            DirectAccess.Write(new[] { CTRL_REG6, (byte)MagneticScale });
            DirectAccess.Write(new[] { CTRL_REG7, (byte)MagneticMode });
        }
    }

    internal sealed class SixAxisAccelerometerAndCompassConfiguration : ISixAxisAccelerometerAndCompassConfiguration
    {
        private readonly SixAxisAccelerometerAndCompass _sensor;

        public SixAxisAccelerometerAndCompassConfiguration(SixAxisAccelerometerAndCompass sensor)
        {
            _sensor = sensor;
        }

        public void AccelerationAxes(AccelerationAxes value)
        {
            _sensor.AccelerationAxes = value;
        }

        public void AccelerationDataRate(AccelerationDataRate value)
        {
            _sensor.AccelerationDataRate = value;
        }

        public void AccelerationDataUpdateMode(AccelerationDataUpdateMode value)
        {
            _sensor.AccelerationDataUpdateMode = value;
        }

        public void AccelerationScale(AccelerationScale value)
        {
            _sensor.AccelerationScale = value;
        }

        public void MagneticDataRate(MagneticDataRate value)
        {
            if ((value == Configuration.MagneticDataRate.Hz_100) && (_sensor.AccelerationDataRate > Configuration.AccelerationDataRate.None) && (_sensor.AccelerationDataRate <= Configuration.AccelerationDataRate.Hz_50))
            {
                _sensor.AccelerationDataRate = Configuration.AccelerationDataRate.Hz_100;
            }

            _sensor.MagneticDataRate = value;
        }

        public void MagneticMode(MagneticMode value)
        {
            _sensor.MagneticMode = value;
        }

        public void MagneticResolution(MagneticResolution value)
        {
            _sensor.MagneticResolution = value;
        }

        public void MagneticScale(MagneticScale value)
        {
            _sensor.MagneticScale = value;
        }
    }

    namespace Configuration
    {
        [Flags]
        public enum AccelerationAxes : byte
        {
            None = 0,
            X = 4,
            Y = 2,
            Z = 1,
            XYZ = X | Y | Z
        }

        public enum AccelerationDataRate : byte
        {
            None = 0,
            Hz_3_125 = 16,
            Hz_6_25 = 32,
            Hz_12_5 = 48,
            Hz_25 = 64,
            Hz_50 = 80,
            Hz_100 = 96,
            Hz_200 = 112,
            Hz_400 = 128,
            Hz_800 = 144,
            Hz_1600 = 160
        }

        public enum AccelerationDataUpdateMode : byte
        {
            Continuous = 0,
            OnRead = 8
        }

        public enum AccelerationScale : byte
        {
            G_2 = 0,
            G_4 = 8,
            G_6 = 16,
            G_8 = 24,
            G_16 = 32
        }

        public enum MagneticMode : byte
        {
            ContinousConversion = 0,
            SingleConversion = 1,
            PowerDown = 3
        }

        public enum MagneticDataRate : byte
        {
            Hz_3_125 = 0,
            Hz_6_25 = 4,
            Hz_12_5 = 8,
            Hz_25 = 12,
            Hz_50 = 16,
            Hz_100 = 20
        }

        public enum MagneticResolution : byte
        {
            Low = 0,
            High = 96
        }

        public enum MagneticScale : byte
        {
            Gs_2 = 0,
            Gs_4 = 32,
            Gs_8 = 64,
            Gs_12 = 96
        }
    }
}