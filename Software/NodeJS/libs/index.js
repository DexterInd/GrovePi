module.exports.GrovePi = {
    commands: require('./commands')
  , board: require('./grovepi')
  , sensors: {
      base: {
          Sensor: require('./sensors/base/sensor')
        , Analog: require('./sensors/base/analogSensor')
        , Digital: require('./sensors/base/digitalSensor')
        , I2C: require('./sensors/base/i2cSensor')
      }
    , DigitalInput: require('./sensors/genericDigitalInputSensor')
    , DigitalOutput: require('./sensors/genericDigitalOutputSensor')
    , AccelerationI2C: require('./sensors/accelerationI2cSensor')
    , AirQualityAnalog: require('./sensors/airQualityAnalogSensor')
    , ChainableRGBLedDigital: require('./sensors/chainableRGBLedDigitalSensor')
    , DHTDigital: require('./sensors/DHTDigitalSensor')
    , FourDigitDigital: require('./sensors/fourDigitDigitalSensor')
    , LedBarDigital: require('./sensors/ledBarDigitalSensor')
    , LightAnalog: require('./sensors/lightAnalogSensor')
    , RTCI2C: require('./sensors/rtcI2cSensor')
    , TemperatureAnalog: require('./sensors/temperatureAnalogSensor')
    , UltrasonicDigital: require('./sensors/ultrasonicDigitalSensor')
    , IRReceiver: require('./sensors/IRReceiverSensor')
    , SPDTRelay: require('./sensors/SPDTRelay')
    , dustDigital: require('./sensors/dustDigitalSensor')
    , encoderDigital: require('./sensors/encoderDigitalSensor')
    , waterFlowDigital: require('./sensors/waterFlowDigitalSensor')
  }
}
