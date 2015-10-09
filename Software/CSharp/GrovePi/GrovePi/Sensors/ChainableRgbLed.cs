using System;

namespace GrovePi.Sensors
{
    public interface IChainableRgbLed
    {
        IChainableRgbLed Initialise(byte numberOfLeds);
        IChainableRgbLed StoreColor(byte red, byte green, byte blue);
        IChainableRgbLed Test(byte numberOfLeds, byte testColor);
        IChainableRgbLed SetPattern(byte pattern, byte led);
        IChainableRgbLed Mudulo(byte offset, byte divisor);
        IChainableRgbLed SetLevel(byte level, bool reverse);
    }

    internal class ChainableRgbLed : IChainableRgbLed
    {
        public const byte StoreColorCommandAddress = 90;
        public const byte InitialiseCommandAddress = 91;
        public const byte TestCommandAddress = 92;
        public const byte SetPatternCommandAddress = 93;
        public const byte SetModuloCommandAddress = 94;
        public const byte SetLevelCommmandAddress = 95;
        private readonly GrovePi _device;
        private readonly Pin _pin;

        internal ChainableRgbLed(GrovePi device, Pin pin)
        {
            if (device == null) throw new ArgumentNullException(nameof(device));
            _device = device;
            _pin = pin;
        }

        public IChainableRgbLed SetLevel(byte level, bool reverse)
        {
            var buffer = new[] {level, (byte) _pin, level, reverse ? (byte) 1 : (byte) 0};
            _device.DirectAccess.Write(buffer);
            return this;
        }

        public IChainableRgbLed Initialise(byte numberOfLeds)
        {
            var buffer = new[] {InitialiseCommandAddress, (byte) _pin, numberOfLeds, Constants.Unused};
            _device.DirectAccess.Write(buffer);
            return this;
        }

        public IChainableRgbLed StoreColor(byte red, byte green, byte blue)
        {
            var buffer = new[] {StoreColorCommandAddress, red, green, blue};
            _device.DirectAccess.Write(buffer);
            return this;
        }

        public IChainableRgbLed Test(byte numberOfLeds, byte testColor)
        {
            var buffer = new[] {TestCommandAddress, (byte) _pin, numberOfLeds, testColor};
            _device.DirectAccess.Write(buffer);
            return this;
        }

        public IChainableRgbLed SetPattern(byte pattern, byte led)
        {
            var buffer = new[] {SetPatternCommandAddress, (byte) _pin, pattern, led};
            _device.DirectAccess.Write(buffer);
            return this;
        }

        public IChainableRgbLed Mudulo(byte offset, byte divisor)
        {
            var buffer = new[] {SetModuloCommandAddress, (byte) _pin, offset, divisor};
            _device.DirectAccess.Write(buffer);
            return this;
        }
    }
}