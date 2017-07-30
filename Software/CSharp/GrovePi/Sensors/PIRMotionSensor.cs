namespace GrovePi.Sensors
{
    public interface IPIRMotionSensor
    {
        bool IsPeopleDetected();
    }

    internal class PIRMotionSensor:Sensor<IPIRMotionSensor>, IPIRMotionSensor
    {
        public PIRMotionSensor(GrovePi device, Pin pin):base(device, pin, PinMode.Input)
        {

        }

        public bool IsPeopleDetected()
        {
            int sensorValue = Device.DigitalRead(Pin);
            if (sensorValue == 0)
            {
                return false;
            }
            else
            {
                return true;
            }
        }
    }
}
