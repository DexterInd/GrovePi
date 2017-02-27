﻿using System;
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
        ITemperatureSensor TemperatureSensor(Pin pin);
        ITemperatureAndHumiditySensor TemperatureAndHumiditySensor(Pin pin, Model model);
        IDHTTemperatureAndHumiditySensor DHTTemperatureAndHumiditySensor(Pin pin, DHTModel model);
        IUltrasonicRangerSensor UltraSonicSensor(Pin pin);
        IAccelerometerSensor AccelerometerSensor(Pin pin);
        IAirQualitySensor AirQualitySensor(Pin pin);
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
        ISixAxisAccelerometerAndCompass SixAxisAccelerometerAndCompass();
        IPIRMotionSensor PIRMotionSensor(Pin pin);
        IGasSensorMQ2 GasSensorMQ2(Pin pin);
        IMiniMotorDriver MiniMotorDriver();
        IOLEDDisplay9696 OLEDDisplay9696();
        IThreeAxisAccelerometerADXL345 ThreeAxisAccelerometerADXL345();
    }

    internal class DeviceBuilder : IBuildGroveDevices
    {
        private const string I2CName = "I2C1"; /* For Raspberry Pi 2, use I2C1 */
        private const byte GrovePiAddress = 0x04;
        private const byte DisplayRgbI2CAddress = 0x62;
        private const byte DisplayTextI2CAddress = 0x3e;
        private const byte SixAxisAccelerometerI2CAddress = 0x1e;
        private const byte MiniMotorDriverI2cAddress1 = 0x62;  // 0xC4
        private const byte MiniMotorDriverI2cAddress2 = 0x60;  // 0xC0
        private const byte OLED96_96I2cAddress = 0x3C;
        private const byte ThreeAxisAccelemeterADXL345I2cAddress = 0x53;
        private GrovePi _device;
        private RgbLcdDisplay _rgbLcdDisplay;
        private SixAxisAccelerometerAndCompass _sixAxisAccelerometerAndCompass;
        private MiniMotorDriver _miniMotorDriver;
        private OLEDDisplay9696 _oledDisplay9696;
        private ThreeAxisAccelerometerADXL345 _ThreeAxisAccelerometerADXL345;

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

        public ITemperatureSensor TemperatureSensor(Pin pin)
        {
            return DoBuild(x => new TemperatureSensor(x, pin));
        }

        public ITemperatureAndHumiditySensor TemperatureAndHumiditySensor(Pin pin, Model model)
        {
            return DoBuild(x => new TemperatureAndHumiditySensor(x, pin, model));
        }

        public IDHTTemperatureAndHumiditySensor DHTTemperatureAndHumiditySensor(Pin pin, DHTModel model)
        {
            return DoBuild(x => new DHTTemperatureAndHumiditySensor(x, pin, model));
        }

        public IAirQualitySensor AirQualitySensor(Pin pin)
        {
            return DoBuild(x => new AirQualitySensor(x, pin));
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

        public ISixAxisAccelerometerAndCompass SixAxisAccelerometerAndCompass()
        {
            return BuildSixAxisAccelerometerAndCompassImpl();
        }

        public IMiniMotorDriver MiniMotorDriver()
        {
            return BuildMiniMotorDriverImpl(MiniMotorDriverI2cAddress1, MiniMotorDriverI2cAddress2);
        }

        public IMiniMotorDriver MiniMotorDriver(int address1, int address2)
        {
            return BuildMiniMotorDriverImpl(address1, address2);
        }

        public IOLEDDisplay9696 OLEDDisplay9696()
        {
            return BuildOLEDDisplayImpl();
        }

        public IThreeAxisAccelerometerADXL345 ThreeAxisAccelerometerADXL345()
        {
            return BuildThreeAxisAccelerometerADXL345Impl();
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

        private SixAxisAccelerometerAndCompass BuildSixAxisAccelerometerAndCompassImpl()
        {
            if (_sixAxisAccelerometerAndCompass != null)
            {
                return _sixAxisAccelerometerAndCompass;
            }

            var settings = new I2cConnectionSettings(SixAxisAccelerometerI2CAddress)
            {
                BusSpeed = I2cBusSpeed.StandardMode
            };

            _sixAxisAccelerometerAndCompass = Task.Run(async () =>
            {
                var dis = await GetDeviceInfo();
                var device = await I2cDevice.FromIdAsync(dis[0].Id, settings);

                return new SixAxisAccelerometerAndCompass(device);
            }).Result;

            return _sixAxisAccelerometerAndCompass;
        }

        private MiniMotorDriver BuildMiniMotorDriverImpl(int miniMotorDriverAddress1, int miniMotorDriverAddress2)
        {
            if (_miniMotorDriver != null)
            {
                return _miniMotorDriver;
            }

            var motor1ConnectionSettings = new I2cConnectionSettings(MiniMotorDriverI2cAddress1)
            {
                BusSpeed = I2cBusSpeed.StandardMode
            };
            var motor2ConnectionSettings = new I2cConnectionSettings(MiniMotorDriverI2cAddress2)
            {
                BusSpeed = I2cBusSpeed.StandardMode
            };

            _miniMotorDriver = Task.Run(async () =>
            {
                var dis = await GetDeviceInfo();
                var miniMotor1 = await I2cDevice.FromIdAsync(dis[0].Id, motor1ConnectionSettings);
                var miniMotor2 = await I2cDevice.FromIdAsync(dis[0].Id, motor2ConnectionSettings);
                return new MiniMotorDriver(miniMotor1, miniMotor2);
            }).Result;
            return _miniMotorDriver;
        }

        private OLEDDisplay9696 BuildOLEDDisplayImpl()
        {
            if(_oledDisplay9696 != null)
            {
                return _oledDisplay9696;
            }
            var connectionSettings = new I2cConnectionSettings(OLED96_96I2cAddress)
            {
                BusSpeed = I2cBusSpeed.StandardMode
            };

            _oledDisplay9696 = Task.Run(async () => 
            {
                var dis = await GetDeviceInfo();

                var device = await I2cDevice.FromIdAsync(dis[0].Id, connectionSettings);
                return new OLEDDisplay9696(device);
            }).Result;
            return _oledDisplay9696;
        }

        private ThreeAxisAccelerometerADXL345 BuildThreeAxisAccelerometerADXL345Impl()
        {
            if (_ThreeAxisAccelerometerADXL345 != null)
            {
                return _ThreeAxisAccelerometerADXL345;
            }
            var connectionSettings = new I2cConnectionSettings(ThreeAxisAccelemeterADXL345I2cAddress)
            {
                BusSpeed = I2cBusSpeed.StandardMode
            };

            _ThreeAxisAccelerometerADXL345 = Task.Run(async () =>
            {
                var dis = await GetDeviceInfo();

                var device = await I2cDevice.FromIdAsync(dis[0].Id, connectionSettings);
                return new ThreeAxisAccelerometerADXL345(device);
            }).Result;
            return _ThreeAxisAccelerometerADXL345;
        }

        private static async Task<DeviceInformationCollection> GetDeviceInfo()
        {
            //Find the selector string for the I2C bus controller
            var aqs = I2cDevice.GetDeviceSelector(I2CName);
            //Find the I2C bus controller device with our selector string
            var dis = await DeviceInformation.FindAllAsync(aqs);
            return dis;
        }

        public IPIRMotionSensor PIRMotionSensor(Pin pin)
        {
            return DoBuild(x => new PIRMotionSensor(x, pin));
        }

        public IGasSensorMQ2 GasSensorMQ2(Pin pin)
        {
            return DoBuild(x => new GasSensorMQ2(x, pin));
        }
    }
}