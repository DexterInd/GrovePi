var util         = require('util')
var Sensor       = require('./sensor')
var commands     = require('../../commands')

function DigitalSensor(pin) {
  Sensor.apply(this, Array.prototype.slice.call(arguments))
  this.pin = pin
}
util.inherits(DigitalSensor, Sensor)
DigitalSensor.prototype = new DigitalSensor()

DigitalSensor.prototype.read = function() {
  var writeRet = this.board.writeBytes(commands.dRead.concat([this.pin, commands.unused, commands.unused]))
  if (writeRet) {
    this.board.wait(100)
    return this.board.readByte()[0]
  } else {
    return false
  }
}
DigitalSensor.prototype.write = function(value) {
  return this.board.writeBytes(commands.dWrite.concat([this.pin, value, commands.unused]))
}

module.exports = DigitalSensor
