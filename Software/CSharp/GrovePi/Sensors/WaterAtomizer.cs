namespace GrovePi.Sensors
{
    public interface IWaterAtomizer
    {
        SensorStatus CurrentState { get; }
        IWaterAtomizer ChangeState(SensorStatus newState);
    }

    internal class WaterAtomizer : Sensor<IWaterAtomizer>, IWaterAtomizer
    {
        public WaterAtomizer(IGrovePi device, Pin pin) : base(device, pin, PinMode.Output)
        { }
    }
}