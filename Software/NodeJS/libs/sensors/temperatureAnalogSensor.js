var AnalogSensor = require('./base/analogSensor')
var commands     = require('../commands')

function TemperatureAnalogSensor(pin) {
  AnalogSensor.apply(this, Array.prototype.slice.call(arguments))
}
TemperatureAnalogSensor.prototype = new AnalogSensor()

TemperatureAnalogSensor.prototype.read = function() {
  var res = AnalogSensor.prototype.read.call(this)
  var resistance = (1023-res) * 10000 / res
  return (1 / (Math.log(resistance / 10000) / 3975 + 1 / 298.15) - 273.15)
}

module.exports = TemperatureAnalogSensor