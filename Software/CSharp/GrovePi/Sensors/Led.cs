namespace GrovePi.Sensors
{
    public interface ILed
    {
        SensorStatus CurrentState { get; }
        ILed ChangeState(SensorStatus newState);
        void AnalogWrite(byte value);
    }

    internal class Led : Sensor<ILed>, ILed
    {
        internal Led(IGrovePi device, Pin pin) : base(device, pin, PinMode.Output)
        {
        }
    }
}