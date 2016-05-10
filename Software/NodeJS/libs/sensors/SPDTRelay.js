var DigitalSensor = require('./base/digitalSensor'),
    commands = require('../commands')

function SPDTRelay(pin) {
    DigitalSensor.apply(this, Array.prototype.slice.call(arguments))
}
SPDTRelay.prototype = new DigitalSensor()

SPDTRelay.prototype.on = function () {
    this.board.pinMode(this.board.OUTPUT)
    var write = this.board.writeBytes(commands.dWrite.concat([this.pin, 1, commands.unused]))
    if (write) {
        return true
    } else {
        return false
    }
}

SPDTRelay.prototype.off = function () {
    this.board.pinMode(this.board.OUTPUT)
    var write = this.board.writeBytes(commands.dWrite.concat([this.pin, 0, commands.unused]))
    if (write) {
        return true
    } else {
        return false
    }
}

module.exports = SPDTRelay