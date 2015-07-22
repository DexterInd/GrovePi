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
GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
Copyright (C) 2015  Dexter Industries

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/gpl-3.0.txt>.
