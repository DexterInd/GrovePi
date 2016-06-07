// Thanks to Craig Watkins for the contribution
var DigitalSensor = require('./base/digitalSensor')
var commands      = require('../commands')

function GenericDigitalInputSensor(pin) {
  DigitalSensor.apply(this, Array.prototype.slice.call(arguments))
}
GenericDigitalInputSensor.prototype = new DigitalSensor()

GenericDigitalInputSensor.prototype.read = function() {
    return DigitalSensor.prototype.read.call(this)
}

module.exports = GenericDigitalInputSensor
