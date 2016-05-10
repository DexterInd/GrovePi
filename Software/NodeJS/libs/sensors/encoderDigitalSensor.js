// TODO: call disable function on exit
var DigitalSensor = require('./base/digitalSensor')
var commands     = require('../commands')

function EncoderDigitalSensor(pin) {
  DigitalSensor.apply(this, Array.prototype.slice.call(arguments))
}
EncoderDigitalSensor.prototype = new DigitalSensor()

EncoderDigitalSensor.prototype.read = function() {
  var write = this.board.writeBytes(commands.encoderRead.concat([this.pin, commands.unused, commands.unused]))
  if (write) {
    this.board.wait(200)
    this.board.readByte()
    var bytes = this.board.readBytes()
    if (bytes instanceof Buffer && bytes[1] != 255)
      return [bytes[1], bytes[2]]
    else
      return false
  } else {
    return false
  }
}
EncoderDigitalSensor.prototype.enable = function() {
  var write = this.board.writeBytes(commands.encoderEn.concat([commands.unused, commands.unused, commands.unused]))
  if (write) {
    this.board.wait(200)
    return true
  } else {
    return false
  }
}
EncoderDigitalSensor.prototype.disable = function() {
  var write = this.board.writeBytes(commands.encoderDis.concat([commands.unused, commands.unused, commands.unused]))
  if (write) {
    this.board.wait(200)
    return true
  } else {
    return false
  }
}

module.exports = EncoderDigitalSensor