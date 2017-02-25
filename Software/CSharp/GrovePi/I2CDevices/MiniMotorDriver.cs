using System;
using Windows.Devices.I2c;

namespace GrovePi.I2CDevices
{
    public interface IMiniMotorDriver
    {
        IMiniMotorDriver drive1(int Speed);
        IMiniMotorDriver drive2(int Speed);
        //IMiniMotorDriver getFault();
    }

    internal sealed class MiniMotorDriver : IMiniMotorDriver
    {
        internal MiniMotorDriver(I2cDevice Motor1Device, I2cDevice Motor2Device)
        {
            if (Motor1Device == null) throw new ArgumentNullException(nameof(Motor1Device));
            motor1DirectAccess = Motor1Device;

            if (Motor2Device == null) throw new ArgumentNullException(nameof(Motor2Device));
            motor2DirectAccess = Motor2Device;
        }

        ~MiniMotorDriver()
        {
            this.drive1(0);
            this.drive2(0);
        }

        internal I2cDevice motor1DirectAccess { get; }
        internal I2cDevice motor2DirectAccess { get; }

        public IMiniMotorDriver drive1(int Speed)
        {
            byte regValue = 0x80;
            motor1DirectAccess.Write(new byte[] { 0x1, regValue });
            regValue = (byte)Math.Abs(Speed);
            if (regValue > 63) regValue = 63;
            regValue = (byte)(regValue * 4);
            if (Speed < 0) regValue |= 0x01;
            else regValue |= 0x02;
            motor1DirectAccess.Write(new byte[] { 0x00, regValue});

            return this;
        }

        public IMiniMotorDriver drive2(int Speed)
        {
            byte regValue = 0x80;
            motor2DirectAccess.Write(new byte[] { 0x1, regValue });
            regValue = (byte)Math.Abs(Speed);
            if (regValue > 63) regValue = 63;
            regValue = (byte)(regValue * 4);
            if (Speed < 0) regValue |= 0x01;
            else regValue |= 0x02;
            motor2DirectAccess.Write(new byte[] { 0x00, regValue });

            return this;
        }
    }
}
