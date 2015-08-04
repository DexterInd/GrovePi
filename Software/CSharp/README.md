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

## License

The MIT License (MIT)

GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
Copyright (C) 2015  Dexter Industries

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
