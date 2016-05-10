var util         = require('util')
var Sensor       = require('./sensor')
var commands     = require('../../commands')

function AnalogSensor(pin) {
  Sensor.apply(this, Array.prototype.slice.call(arguments))
  this.pin = pin
}
util.inherits(AnalogSensor, Sensor)
AnalogSensor.prototype = new AnalogSensor()

AnalogSensor.prototype.read = function(length) {
  if (typeof length == 'undefined')
    length = this.board.BYTESLEN

  var writeRet = this.board.writeBytes(commands.aRead.concat([this.pin, commands.unused, commands.unused]))
  if (writeRet) {
    this.board.readByte()
    var bytes = this.board.readBytes(length)
    if (bytes instanceof Buffer) {
      return bytes[1] * 256 + bytes[2]
    } else {
      return false
    }
  } else {
    return false
  }
}
AnalogSensor.prototype.write = function(value) {
  return this.board.writeBytes(commands.aWrite.concat([this.pin, value, commands.unused]))
}

module.exports = AnalogSensor