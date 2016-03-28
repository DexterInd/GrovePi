using System;
using Windows.Devices.I2c;

using GrovePi.Common;

namespace GrovePi
{
    public interface IGrovePi
    {
        string GetFirmwareVersion();
        byte DigitalRead(Pin pin);
        void DigitalWrite(Pin pin, byte value);
        int AnalogRead(Pin pin);
        void AnalogWrite(Pin pin, byte value);
        void PinMode(Pin pin, PinMode mode);
        void Flush();
    }

    internal sealed class GrovePi : IGrovePi
    {
        internal GrovePi(I2cDevice device)
        {
            if (device == null) throw new ArgumentNullException(nameof(device));
            DirectAccess = device;
        }

        internal I2cDevice DirectAccess { get; }

        public string GetFirmwareVersion()
        {
            var wbuffer = new byte[4] {(byte) Command.Version, Constants.Unused, Constants.Unused, Constants.Unused};
            var rbuffer = new byte[4];
            var i2cTransferResult = DirectAccess.WritePartial(wbuffer);
            if (i2cTransferResult.Status != I2cTransferStatus.FullTransfer)
            {
                return "0.0.0";
            }
            i2cTransferResult = DirectAccess.ReadPartial(rbuffer);
            if (i2cTransferResult.Status != I2cTransferStatus.FullTransfer)
            {
                return "0.0.0";
            }
            return $"{rbuffer[1]}.{rbuffer[2]}.{rbuffer[3]}";
        }

        public byte DigitalRead(Pin pin)
        {
            var wbuffer = new byte[4] {(byte) Command.DigitalRead, (byte) pin, Constants.Unused, Constants.Unused};
            var rBuffer = new byte[1];
            var i2cTransferResult = DirectAccess.WritePartial(wbuffer);
            Delay.Milliseconds(10);
            if (i2cTransferResult.Status != I2cTransferStatus.FullTransfer)
            {
                return 0;
            }
            i2cTransferResult = DirectAccess.ReadPartial(rBuffer);
            if (i2cTransferResult.Status != I2cTransferStatus.FullTransfer)
            {
                return 0;
            }

            return rBuffer[0];
        }

        public void DigitalWrite(Pin pin, byte value)
        {
            var buffer = new byte[4] {(byte) Command.DigitalWrite, (byte) pin, value, Constants.Unused};
            DirectAccess.WritePartial(buffer);
            Delay.Milliseconds(10);
        }

        public int AnalogRead(Pin pin)
        {
            var wbuffer = new byte[4]{(byte) Command.AnalogRead, (byte) pin, Constants.Unused, Constants.Unused};
            var rbuffer = new byte[3];
            var i2cTransferResult  = DirectAccess.WritePartial(wbuffer);
            Delay.Milliseconds(10);
            if (i2cTransferResult.Status != I2cTransferStatus.FullTransfer)
            {
                return 0;
            }
            i2cTransferResult = DirectAccess.ReadPartial(rbuffer);
            if (i2cTransferResult.Status != I2cTransferStatus.FullTransfer)
            {
                return 0;
            }

            return rbuffer[1]*256 + rbuffer[2];
        }

        public void AnalogWrite(Pin pin, byte value)
        {
            var buffer = new byte[4] {(byte) Command.AnalogWrite, (byte) pin, value, Constants.Unused};
            DirectAccess.WritePartial(buffer);
            Delay.Milliseconds(10);
        }

        public void PinMode(Pin pin, PinMode mode)
        {
            var buffer = new byte[4] {(byte) Command.PinMode, (byte) pin, (byte) mode, Constants.Unused};
            DirectAccess.WritePartial(buffer);
            Delay.Milliseconds(10);
        }

        public void Flush()
        {
            var buffer = new byte[4] { Constants.Unused, Constants.Unused, Constants.Unused, Constants.Unused };
            DirectAccess.WritePartial(buffer);
        }

        private enum Command
        {
            DigitalRead = 1,
            DigitalWrite = 2,
            AnalogRead = 3,
            AnalogWrite = 4,
            PinMode = 5,
            Version = 8,
            //DhtProSensorTemp = 40,
        };
    }
}