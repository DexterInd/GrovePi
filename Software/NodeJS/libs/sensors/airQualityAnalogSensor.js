var AnalogSensor = require('./base/analogSensor')
var commands     = require('../commands')

function AirQualityAnalogSensor(pin) {
  AnalogSensor.apply(this, Array.prototype.slice.call(arguments))
}
AirQualityAnalogSensor.prototype = new AnalogSensor()

AirQualityAnalogSensor.prototype.read = function() {
  this.board.pinMode(this.board.INPUT)
  var res = AnalogSensor.prototype.read.call(this)
  return parseInt(res)
}

module.exports = AirQualityAnalogSensor