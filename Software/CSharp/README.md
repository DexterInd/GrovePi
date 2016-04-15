# GrovePi
Windows 10 IoT C# driver library for GrovePi

The NuGet package for the current release is available [here](https://www.nuget.org/packages/GrovePi/).

All supported sensors are available through the DeviceFactory class.

Supported sensors include:
- Relay
- Led
- TemperatureAndHumiditySensor
- UltraSonicSensor
- AccelerometerSensor
- RealTimeClock
- BuildLedBar
- FourDigitDisplay
- ChainableRgbLed
- RotaryAngleSensor
- Buzzer
- SoundSensor
- LightSensor
- ButtonSensor
- RgbLcdDisplay

#####Examples
Below are some simple examples of how to use the library.

######Measure Distance
Ultra sonic sensor plugged into digital pin 2 (D2)
<p>
<code>
  var distance = DeviceFactory.Build.UltraSonicSensor(Pin.DigitalPin2).MeasureInCentimeters();
</code>
</p>

######Display Hello World
<code>
  DeviceFactory.Build.RgbLcdDisplay().SetText("Hello World").SetBacklightRgb(0, 255, 255);
</code>

######Sound the buzzer!
Sound the buzzer plugged into digital pin 2 (D2)
<p>
<code>
  DeviceFactory.Build.Buzzer(Pin.DigitalPin2).ChangeState(SensorStatus.On);
</code>
</p>
