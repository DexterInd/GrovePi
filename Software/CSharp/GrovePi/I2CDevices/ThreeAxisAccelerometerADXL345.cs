using System;
using GrovePi.I2CDevices.Configuration;
using Windows.Devices.I2c;

namespace GrovePi.I2CDevices
{

    public interface IThreeAxisAccelerometerADXL345
    {
        IThreeAxisAccelerometerADXL345 Initialize();
        double[] GetAcclXYZ();
    }

    internal sealed class ThreeAxisAccelerometerADXL345 : IThreeAxisAccelerometerADXL345
    {
        struct Acceleration
        {
            public double X;
            public double Y;
            public double Z;
        };

        private const byte ACCEL_I2C_ADDR = 0x53;           /* 7-bit I2C address of the ADXL345 with SDO pulled low */
        private const byte ACCEL_REG_POWER_CONTROL = 0x2D;  /* Address of the Power Control register */
        private const byte ACCEL_REG_DATA_FORMAT = 0x31;    /* Address of the Data Format register   */
        private const byte ACCEL_REG_X = 0x32;              /* Address of the X Axis data register   */
        private const byte ACCEL_REG_Y = 0x34;              /* Address of the Y Axis data register   */
        private const byte ACCEL_REG_Z = 0x36;              /* Address of the Z Axis data register   */

        internal I2cDevice DirectAccess { get; }

        internal ThreeAxisAccelerometerADXL345(I2cDevice Device)
        {
            if (Device == null) throw new ArgumentNullException(nameof(Device));

            DirectAccess = Device;
        }

        public IThreeAxisAccelerometerADXL345 Initialize()
        {
            /* 
             * Initialize the accelerometer:
             *
             * For this device, we create 2-byte write buffers:
             * The first byte is the register address we want to write to.
             * The second byte is the contents that we want to write to the register. 
             */
            byte[] WriteBuf_DataFormat = new byte[] {  ACCEL_REG_DATA_FORMAT, 0x01 };        /* 0x01 sets range to +- 4Gs                         */
            byte[] WriteBuf_PowerControl = new byte[] {  ACCEL_REG_POWER_CONTROL, 0x08 };    /* 0x08 puts the accelerometer into measurement mode */

            /* Write the register settings */
            DirectAccess.Write(WriteBuf_DataFormat);
            DirectAccess.Write(WriteBuf_PowerControl);

            return this;
        }

        public double[] GetAcclXYZ()
        {
            const int ACCEL_RES = 1024;         /* The ADXL345 has 10 bit resolution giving 1024 unique values                     */
            const int ACCEL_DYN_RANGE_G = 8;    /* The ADXL345 had a total dynamic range of 8G, since we're configuring it to +-4G */
            const int UNITS_PER_G = ACCEL_RES / ACCEL_DYN_RANGE_G;  /* Ratio of raw int values to G units                          */

            byte[] RegAddrBuf = new byte[] { ACCEL_REG_X }; /* Register address we want to read from                                         */
            byte[] ReadBuf = new byte[6];                   /* We read 6 bytes sequentially to get all 3 two-byte axes registers in one read */
            
            /* 
             * Read from the accelerometer 
             * We call WriteRead() so we first write the address of the X-Axis I2C register, then read all 3 axes
             */
            DirectAccess.WriteRead(RegAddrBuf, ReadBuf);

            /* 
             * In order to get the raw 16-bit data values, we need to concatenate two 8-bit bytes from the I2C read for each axis.
             * We accomplish this by using the BitConverter class.
             */
            short AccelerationRawX = BitConverter.ToInt16(ReadBuf, 0);
            short AccelerationRawY = BitConverter.ToInt16(ReadBuf, 2);
            short AccelerationRawZ = BitConverter.ToInt16(ReadBuf, 4);

            /* Convert raw values to G's */
            double[] accel = new double[3];
            accel[0] = (double)AccelerationRawX / UNITS_PER_G;
            accel[1] = (double)AccelerationRawY / UNITS_PER_G;
            accel[2] = (double)AccelerationRawZ / UNITS_PER_G;

            return accel;
        }
        
    }
}