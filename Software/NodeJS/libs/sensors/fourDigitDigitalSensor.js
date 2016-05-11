var DigitalSensor = require('./base/digitalSensor')
var commands     = require('../commands')

function FourDigitDigitalSensor(pin) {
  DigitalSensor.apply(this, Array.prototype.slice.call(arguments))
}
FourDigitDigitalSensor.prototype = new DigitalSensor()

FourDigitDigitalSensor.prototype.init = function() {
  this.board.pinMode(this.board.OUTPUT)
  return this.board.writeBytes(commands.fourDigitInit.concat([this.pin, commands.unused, commands.unused]))
}
FourDigitDigitalSensor.prototype.setNumber = function(value, useLeadingZero) {
  this.board.pinMode(this.board.OUTPUT)
  var byte1 = value & 255
  var byte2 = value >> 8
  var command = useLeadingZero ? commands.fourDigitValue : commands.fourDigitValueZeros
  var write = this.board.writeBytes(command.concat([this.pin, byte1, byte2]))
  if (write) {
    this.board.wait(500)
    return true
  } else {
    return false
  }
}
FourDigitDigitalSensor.prototype.setBrightness = function(brightness) {
  this.board.pinMode(this.board.OUTPUT)
  var write = this.board.writeBytes(commands.fourDigitBrightness.concat([this.pin, brightness, commands.unused]))
  if (write) {
    this.board.wait(500)
    return true
  } else {
    return false
  }
}
FourDigitDigitalSensor.prototype.setDigit = function(segment, value) {
  this.board.pinMode(this.board.OUTPUT)
  var write = this.board.writeBytes(commands.fourDigitIndividualDigit.concat([this.pin, segment, value]))
  if (write) {
    this.board.wait(500)
    return true
  } else {
    return false
  }
}
FourDigitDigitalSensor.prototype.setSegment = function(segment, leds) {
  this.board.pinMode(this.board.OUTPUT)
  var write = this.board.writeBytes(commands.fourDigitIndividualLeds.concat([this.pin, segment, leds]))
  if (write) {
    this.board.wait(500)
    return true
  } else {
    return false
  }
}
FourDigitDigitalSensor.prototype.setScore = function(left, right) {
  this.board.pinMode(this.board.OUTPUT)
  var write = this.board.writeBytes(commands.fourDigitScore.concat([this.pin, left, right]))
  if (write) {
    this.board.wait(500)
    return true
  } else {
    return false
  }
}
FourDigitDigitalSensor.prototype.monitor = function(analog, duration) {
  this.board.pinMode(this.board.OUTPUT)
  var write = this.board.writeBytes(commands.fourDigitAnalogRead.concat([this.pin, analog, duration]))
  if (write) {
    this.board.wait(duration/1000 + 500) // TODO: This should be tested
    return true
  } else {
    return false
  }
}
FourDigitDigitalSensor.prototype.on = function() {
  this.board.pinMode(this.board.OUTPUT)
  var write = this.board.writeBytes(commands.fourDigitAllOn.concat([this.pin, commands.unused, commands.unused]))
  if (write) {
    this.board.wait(500)
    return true
  } else {
    return false
  }
}
FourDigitDigitalSensor.prototype.off = function() {
  this.board.pinMode(this.board.OUTPUT)
  var write = this.board.writeBytes(commands.fourDigitAllOff.concat([this.pin, commands.unused, commands.unused]))
  if (write) {
    this.board.wait(500)
    return true
  } else {
    return false
  }
}

module.exports = FourDigitDigitalSensor