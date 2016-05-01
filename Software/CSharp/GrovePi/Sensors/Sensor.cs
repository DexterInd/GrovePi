using System;

namespace GrovePi.Sensors
{
    public abstract class Sensor<TSensorType> where TSensorType : class
    {
        protected readonly IGrovePi Device;
        protected readonly Pin Pin;

        internal Sensor(IGrovePi device, Pin pin, PinMode pinMode)
        {
            if (device == null) throw new ArgumentNullException(nameof(device));
            Device = device;
            Pin = pin;
            device.PinMode(Pin, pinMode);
        }

        internal Sensor(IGrovePi device, Pin pin)
        {
            if (device == null) throw new ArgumentNullException(nameof(device));
            Device = device;
            Pin = pin;
        }

        public SensorStatus CurrentState => (SensorStatus) Device.DigitalRead(Pin);

        public TSensorType ChangeState(SensorStatus newState)
        {
            Device.DigitalWrite(Pin, (byte) newState);
            return this as TSensorType;
        }

        public void AnalogWrite(byte value)
        {
            Device.AnalogWrite(Pin,value);
        }
    }
}