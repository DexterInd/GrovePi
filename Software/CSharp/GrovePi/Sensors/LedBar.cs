using System;

namespace GrovePi.Sensors
{
    public interface ILedBar
    {
        ILedBar Initialize(Orientation orientation);
        ILedBar SetOrientation(Orientation orientation);
        ILedBar SetLevel(byte level);
        ILedBar SetLed(byte level, byte led, SensorStatus state);
        ILedBar ToggleLed(byte led);
    }

    internal class LedBar : ILedBar
    {
        private const byte InitialiseCommandAddress = 50;
        private const byte OrientationCommandAddress = 51;
        private const byte LevelCommandAddress = 52;
        private const byte SetOneCommandAddress = 53;
        private const byte ToggleOneCommandAddress = 54;
        //private const byte SetCommandAddress = 55;
        //private const byte GetCommandAddress = 56;

        private readonly GrovePi _device;
        private readonly Pin _pin;

        internal LedBar(GrovePi device, Pin pin)
        {
            if (device == null) throw new ArgumentNullException(nameof(device));
            _device = device;
            _pin = pin;
        }

        public ILedBar Initialize(Orientation orientation)
        {
            var buffer = new[] {InitialiseCommandAddress, (byte) _pin, (byte) orientation, Constants.Unused};
            _device.DirectAccess.WritePartial(buffer);
            return this;
        }

        public ILedBar SetOrientation(Orientation orientation)
        {
            var buffer = new[] {OrientationCommandAddress, (byte) _pin, (byte) orientation, Constants.Unused};
            _device.DirectAccess.WritePartial(buffer);
            return this;
        }

        public ILedBar SetLevel(byte level)
        {
            level = Math.Min(level, (byte) 10);
            var buffer = new[] {LevelCommandAddress, (byte) _pin, level, Constants.Unused};
            _device.DirectAccess.WritePartial(buffer);
            return this;
        }

        public ILedBar SetLed(byte level, byte led, SensorStatus state)
        {
            var buffer = new[] {SetOneCommandAddress, (byte) _pin, led, (byte) state};
            _device.DirectAccess.WritePartial(buffer);
            return this;
        }

        public ILedBar ToggleLed(byte led)
        {
            var buffer = new[] {ToggleOneCommandAddress, (byte) _pin, led, Constants.Unused};
            _device.DirectAccess.WritePartial(buffer);
            return this;
        }
    }

    public enum Orientation
    {
        RedToGreen = 0,
        GreenToRed = 1
    }
}