using System;

namespace GrovePi.Sensors
{
    public interface IFourDigitDisplay
    {
        IFourDigitDisplay Initialise();
        IFourDigitDisplay SetBrightness(byte brightness);
        IFourDigitDisplay SetIndividualSegment(byte segment, byte value);
        IFourDigitDisplay SetLedsOfSegment(byte segment, byte leds);
        IFourDigitDisplay SetScore(byte left, byte right);
        IFourDigitDisplay AllOn();
        IFourDigitDisplay AllOff();
    }

    internal class FourDigitDisplay : IFourDigitDisplay
    {
        private const byte InitialiseCommandAddress = 70;
        private const byte BrightnessCommandAddress = 71;
        private const byte ValueCommandAddress = 72;
        private const byte ValueZerosCommandAddress = 73;
        private const byte IndividualDigitCommandAddress = 74;
        private const byte IndividualLedsCommandAddress = 75;
        private const byte ScoreCommandAddress = 76;
        private const byte AnalogReadCommandAddress = 77;
        private const byte AllOnCommandAddress = 78;
        private const byte AllOffCommandAddress = 79;
        private readonly GrovePi _device;
        private readonly Pin _pin;

        internal FourDigitDisplay(GrovePi device, Pin pin)
        {
            if (device == null) throw new ArgumentNullException(nameof(device));
            _device = device;
            _pin = pin;
        }

        public IFourDigitDisplay Initialise()
        {
            var buffer = new[] {InitialiseCommandAddress, (byte) _pin, Constants.Unused, Constants.Unused};
            _device.DirectAccess.Write(buffer);
            return this;
        }

        public IFourDigitDisplay SetBrightness(byte brightness)
        {
            brightness = Math.Min(brightness, (byte) 7);
            var buffer = new[] { BrightnessCommandAddress, (byte) _pin, brightness, Constants.Unused};
            _device.DirectAccess.Write(buffer);
            return this;
        }

        public IFourDigitDisplay SetIndividualSegment(byte segment, byte value)
        {
            var buffer = new[] {IndividualDigitCommandAddress, (byte) _pin, segment, value};
            _device.DirectAccess.Write(buffer);
            return this;
        }

        public IFourDigitDisplay SetLedsOfSegment(byte segment, byte leds)
        {
            var buffer = new[] {IndividualLedsCommandAddress, (byte) _pin, segment, leds};
            _device.DirectAccess.Write(buffer);
            return this;
        }

        public IFourDigitDisplay SetScore(byte left, byte right)
        {
            var buffer = new[] {ScoreCommandAddress, (byte) _pin, left, right};
            _device.DirectAccess.Write(buffer);
            return this;
        }

        public IFourDigitDisplay AllOn()
        {
            var buffer = new[] {AllOnCommandAddress, (byte) _pin, Constants.Unused, Constants.Unused};
            _device.DirectAccess.Write(buffer);
            return this;
        }

        public IFourDigitDisplay AllOff()
        {
            var buffer = new[] {AllOffCommandAddress, (byte) _pin, Constants.Unused, Constants.Unused};
            _device.DirectAccess.Write(buffer);
            return this;
        }
    }
}