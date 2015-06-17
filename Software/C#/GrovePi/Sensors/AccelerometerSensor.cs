using System;

namespace GrovePi.Sensors
{
    public interface IAccelerometerSensor
    {
        byte[] Read();
    }

    internal class AccelerometerSensor : IAccelerometerSensor
    {
        private const byte CommandAddress = 20;
        private readonly GrovePi _device;
        private readonly Pin _pin;

        internal AccelerometerSensor(GrovePi device, Pin pin)
        {
            if (device == null) throw new ArgumentNullException(nameof(device));
            _device = device;
            _pin = pin;
        }

        public byte[] Read()
        {
            var buffer = new [] {CommandAddress, (byte) _pin, Constants.Unused, Constants.Unused};
            _device.DirectAccess.Write(buffer);

            var readBuffer = new byte[1];
            _device.DirectAccess.Read(readBuffer);

            if (readBuffer[1] > 32)
                readBuffer[1] = (byte) -(readBuffer[1] - 224);
            if (readBuffer[2] > 32)
                readBuffer[2] = (byte) -(readBuffer[1] - 224);
            if (readBuffer[3] > 32)
                readBuffer[3] = (byte) -(readBuffer[1] - 224);

            return readBuffer;
        }
    }
}