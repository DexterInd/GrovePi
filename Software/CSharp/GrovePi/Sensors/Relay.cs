namespace GrovePi.Sensors
{
    public interface IRelay
    {
        SensorStatus CurrentState { get; }
        IRelay ChangeState(SensorStatus newState);
    }
    internal class Relay : Sensor<IRelay>, IRelay
    {
        public Relay(IGrovePi device, Pin pin) : base(device, pin, PinMode.Output)
        {
        }
    }
}
