using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace GrovePi.Sensors
{
    public interface ISoundSensor
    {
        int SensorValue();
    }

    internal class SoundSensor : Sensor<ISoundSensor>, ISoundSensor
    {

        public SoundSensor(IGrovePi device, Pin pin) : base(device, pin, PinMode.Input)
        {
        }

        public int SensorValue()
        {
            return Device.AnalogRead(Pin);
        }
    }
}
