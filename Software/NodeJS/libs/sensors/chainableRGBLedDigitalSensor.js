var DigitalSensor = require('./base/digitalSensor')
var commands     = require('../commands')

function ChainableRGBLedDigitalSensor(pin, numLeds) {
  DigitalSensor.apply(this, Array.prototype.slice.call(arguments))
  this.numLeds
}
ChainableRGBLedDigitalSensor.prototype = new DigitalSensor()

ChainableRGBLedDigitalSensor.prototype.init = function() {
  this.board.pinMode(this.board.OUTPUT)
  var write = this.board.writeBytes(commands.chainableRgbLedInit.concat([this.pin, this.numLeds, commands.unused]))
  if (write) {
    this.board.wait(500)
    return true
  } else {
    return false
  }
}
ChainableRGBLedDigitalSensor.prototype.setPattern = function(pattern, whichLed) {
  this.board.pinMode(this.board.OUTPUT)
  var write = this.board.writeBytes(commands.chainableRgbLedSetPattern.concat([this.pin, pattern, whichLed]))
  if (write) {
    this.board.wait(500)
    return true
  } else {
    return false
  }
}
ChainableRGBLedDigitalSensor.prototype.setModulo = function(offset, divisor) {
  this.board.pinMode(this.board.OUTPUT)
  var write = this.board.writeBytes(commands.chainableRgbLedSetModulo.concat([this.pin, offset, divisor]))
  if (write) {
    this.board.wait(500)
    return true
  } else {
    return false
  }
}
ChainableRGBLedDigitalSensor.prototype.setLevel = function(level, reverse) {
  this.board.pinMode(this.board.OUTPUT)
  var write = this.board.writeBytes(commands.chainableRgbLedSetLevel.concat([this.pin, level, reverse]))
  if (write) {
    this.board.wait(500)
    return true
  } else {
    return false
  }
}


module.exports = ChainableRGBLedDigitalSensor