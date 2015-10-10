namespace GrovePi.Sensors
{
    public interface IButtonSensor
    {
        SensorStatus CurrentState { get; }
    }

    internal class ButtonSensor : Sensor<IButtonSensor>, IButtonSensor
    {
        internal ButtonSensor(IGrovePi device, Pin pin) : base(device, pin, PinMode.Input)
        {
        }
    }
}