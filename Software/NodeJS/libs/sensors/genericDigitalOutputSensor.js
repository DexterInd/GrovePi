// Thanks to Craig Watkins for the contribution
var DigitalSensor = require('./base/digitalSensor')
var commands      = require('../commands')

function GenericDigitalOutputSensor(pin) {
  DigitalSensor.apply(this, Array.prototype.slice.call(arguments))
}
GenericDigitalOutputSensor.prototype = new DigitalSensor()

GenericDigitalOutputSensor.prototype.turnOn = function() {
  this.board.pinMode(this.board.OUTPUT)
  var write = this.board.writeBytes(commands.dWrite.concat([this.pin, 1, commands.unused]))
  if (write) {
    return true
  } else {
    return false
  }
}

GenericDigitalOutputSensor.prototype.turnOff = function() {
  this.board.pinMode(this.board.OUTPUT)
  var write = this.board.writeBytes(commands.dWrite.concat([this.pin, 0, commands.unused]))
  if (write) {
      return true
  } else {
      return false
  }
}

module.exports = GenericDigitalOutputSensor
