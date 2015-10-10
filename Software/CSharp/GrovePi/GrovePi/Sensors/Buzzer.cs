namespace GrovePi.Sensors
{
    public interface IBuzzer
    {
        SensorStatus CurrentState { get; }
        IBuzzer ChangeState(SensorStatus newState);
    }

    internal class Buzzer : Sensor<IBuzzer>, IBuzzer
    {
        internal Buzzer(IGrovePi device, Pin pin) : base(device, pin, PinMode.Output)
        {
        }
    }
}