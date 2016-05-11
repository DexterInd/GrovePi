var AnalogSensor = require('./base/analogSensor')
var commands     = require('../commands')

function LightAnalogSensor(pin) {
  AnalogSensor.apply(this, Array.prototype.slice.call(arguments))
}
LightAnalogSensor.prototype = new AnalogSensor()

LightAnalogSensor.prototype.read = function() {
  var res = AnalogSensor.prototype.read.call(this)
  var number = parseInt(res)
  var resistance = number <= 0 ? 0 : +(Number(parseFloat((1023 - number) * 10 / number)).toFixed(2))
  return resistance
}

module.exports = LightAnalogSensor