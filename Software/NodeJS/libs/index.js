module.exports.GrovePi = {}
module.exports.GrovePi.sensors = {}
module.exports.GrovePi.sensors.base = {}

module.exports.GrovePi.commands = require('./commands.js')

module.exports.GrovePi.board = require('./grovepi.js')

module.exports.GrovePi.sensors.base.Sensor = require('./sensors/base/sensor.js')
module.exports.GrovePi.sensors.base.Analog = require('./sensors/base/analogSensor.js')
module.exports.GrovePi.sensors.base.Digital = require('./sensors/base/digitalSensor.js')
module.exports.GrovePi.sensors.base.I2C = require('./sensors/base/i2cSensor.js')

module.exports.GrovePi.sensors.AccelerationI2C = require('./sensors/accelerationI2cSensor.js')
module.exports.GrovePi.sensors.AirQualityAnalog = require('./sensors/airQualityAnalogSensor.js')
module.exports.GrovePi.sensors.ChainableRGBLedDigital = require('./sensors/chainableRGBLedDigitalSensor.js')
module.exports.GrovePi.sensors.DHTDigital = require('./sensors/DHTDigitalSensor.js')
module.exports.GrovePi.sensors.FourDigitDigital = require('./sensors/fourDigitDigitalSensor.js')
module.exports.GrovePi.sensors.LedBarDigital = require('./sensors/ledBarDigitalSensor.js')
module.exports.GrovePi.sensors.RTCI2C = require('./sensors/rtcI2cSensor.js')
module.exports.GrovePi.sensors.TemperatureAnalog = require('./sensors/temperatureAnalogSensor.js')
module.exports.GrovePi.sensors.UltrasonicDigital = require('./sensors/ultrasonicDigitalSensor.js')