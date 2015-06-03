using System;
using System.Threading.Tasks;
using Windows.Devices.Enumeration;
using Windows.Devices.I2c;
using GrovePi.I2CDevices;
using GrovePi.Sensors;

namespace GrovePi
{
    public static class DeviceFactory
    {
        public static IBuildGroveDevices Build = new DeviceBuilder();
    }

    public interface IBuildGroveDevices
    {
        IGrovePi GrovePi();
        IGrovePi GrovePi(int address);
        IRelay Relay(Pin pin);
        ILed Led(Pin pin);
        ITemperatureAndHumiditySensor TemperatureAndHumiditySensor(Pin pin, Model model);
        IUltrasonicRangerSensor UltraSonicSensor(Pin pin);
        IAccelerometerSensor AccelerometerSensor(Pin pin);
        IRealTimeClock RealTimeClock(Pin pin);
        ILedBar BuildLedBar(Pin pin);
        IFourDigitDisplay FourDigitDisplay(Pin pin);
        IChainableRgbLed ChainableRgbLed(Pin pin);
        IRotaryAngleSensor RotaryAngleSensor(Pin pin);
        IBuzzer Buzzer(Pin pin);
        ISoundSensor SoundSensor(Pin pin);
        ILightSensor LightSensor(Pin pin);
        IButtonSensor ButtonSensor(Pin pin);
        IRgbLcdDisplay RgbLcdDisplay();
        IRgbLcdDisplay RgbLcdDisplay(int rgbAddress, int textAddress);
        
    }

    internal class DeviceBuilder : IBuildGroveDevices
    {
        private const string I2CName = "I2C1"; /* For Raspberry Pi 2, use I2C1 */
        private const byte GrovePiAddress = 0x04;
        private const byte DisplayRgbI2CAddress = 0x62;
        private const byte DisplayTextI2CAddress = 0x3e;
        private GrovePi _device;
        private RgbLcdDisplay _rgbLcdDisplay;

        public IGrovePi GrovePi()
        {
            return BuildGrovePiImpl(GrovePiAddress);
        }

        public IGrovePi GrovePi(int address)
        {
            return BuildGrovePiImpl(address);
        }

        public IRelay Relay(Pin pin)
        {
            return DoBuild(x => new Relay(x, pin));
        }

        public ILed Led(Pin pin)
        {
            return DoBuild(x => new Led(x, pin));
        }

        public ITemperatureAndHumiditySensor TemperatureAndHumiditySensor(Pin pin, Model model)
        {
            return DoBuild(x => new TemperatureAndHumiditySensor(x, pin, model));
        }

        public IUltrasonicRangerSensor UltraSonicSensor(Pin pin)
        {
            return DoBuild(x => new UltrasonicRangerSensor(x, pin));
        }

        public IAccelerometerSensor AccelerometerSensor(Pin pin)
        {
            return DoBuild(x => new AccelerometerSensor(x, pin));
        }

        public IRealTimeClock RealTimeClock(Pin pin)
        {
            return DoBuild(x => new RealTimeClock(x, pin));
        }

        public IRotaryAngleSensor RotaryAngleSensor(Pin pin)
        {
            return DoBuild(x => new RotaryAngleSensor(x, pin));
        }

        public IBuzzer Buzzer(Pin pin)
        {
            return DoBuild(x => new Buzzer(x, pin));
        }

        public ISoundSensor SoundSensor(Pin pin)
        {
            return DoBuild(x => new SoundSensor(x, pin));
        }

        public ILedBar BuildLedBar(Pin pin)
        {
            return DoBuild(x => new LedBar(x, pin));
        }

        public IFourDigitDisplay FourDigitDisplay(Pin pin)
        {
            return DoBuild(x => new FourDigitDisplay(x, pin));
        }

        public IChainableRgbLed ChainableRgbLed(Pin pin)
        {
            return DoBuild(x => new ChainableRgbLed(x, pin));
        }

        public ILightSensor LightSensor(Pin pin)
        {
            return DoBuild(x => new LightSensor(x, pin));
        }

        public IRgbLcdDisplay RgbLcdDisplay(int rgbAddress, int textAddress)
        {
            return BuildRgbLcdDisplayImpl(rgbAddress, textAddress);
        }

        public IRgbLcdDisplay RgbLcdDisplay()
        {
            return BuildRgbLcdDisplayImpl(DisplayRgbI2CAddress, DisplayTextI2CAddress);
        }

        public IButtonSensor ButtonSensor(Pin pin)
        {
            return DoBuild(x => new ButtonSensor(x, pin));
        }

        private TSensor DoBuild<TSensor>(Func<GrovePi, TSensor> factory)
        {
            var device = BuildGrovePiImpl(GrovePiAddress);
            return factory(device);
        }

        private GrovePi BuildGrovePiImpl(int address)
        {
            if (_device != null)
            {
                return _device;
            }

            /* Initialize the I2C bus */
            var settings = new I2cConnectionSettings(address)
            {
                BusSpeed = I2cBusSpeed.StandardMode
            };

            _device = Task.Run(async () =>
            {
                var dis = await GetDeviceInfo();

                // Create an I2cDevice with our selected bus controller and I2C settings
                var device = await I2cDevice.FromIdAsync(dis[0].Id, settings);
                return new GrovePi(device);
            }).Result;
            return _device;
        }

        private RgbLcdDisplay BuildRgbLcdDisplayImpl(int rgbAddress, int textAddress)
        {
            if (null != _rgbLcdDisplay)
            {
                return _rgbLcdDisplay;
            }

            /* Initialize the I2C bus */
            var rgbConnectionSettings = new I2cConnectionSettings(rgbAddress)
            {
                BusSpeed = I2cBusSpeed.StandardMode
            };

            var textConnectionSettings = new I2cConnectionSettings(textAddress)
            {
                BusSpeed = I2cBusSpeed.StandardMode
            };

            _rgbLcdDisplay = Task.Run(async () =>
            {
                var dis = await GetDeviceInfo();

                // Create an I2cDevice with our selected bus controller and I2C settings
                var rgbDevice = await I2cDevice.FromIdAsync(dis[0].Id, rgbConnectionSettings);
                var textDevice = await I2cDevice.FromIdAsync(dis[0].Id, textConnectionSettings);
                return new RgbLcdDisplay(rgbDevice, textDevice);
            }).Result;
            return _rgbLcdDisplay;
        }

        private static async Task<DeviceInformationCollection> GetDeviceInfo()
        {
            //Find the selector string for the I2C bus controller
            var aqs = I2cDevice.GetDeviceSelector(I2CName);
            //Find the I2C bus controller device with our selector string
            var dis = await DeviceInformation.FindAllAsync(aqs);
            return dis;
        }
    }
}