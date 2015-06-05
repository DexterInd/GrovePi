var util         = require('util')
var EventEmitter = require('events').EventEmitter
var Board        = require('../../grovepi')
var streamInterval, watchInterval
var watchDelay = 100

function Sensor() {
  this.board = new Board()
  this.lastValue = 0
  this.currentValue = 0
}

var isEqual = function(a, b) {
  if (typeof a == 'object') {
    for (var i in a) {
      if (a[i] !== b[i]) {
        return false
      }
    }
    return true
  } else {
    return a === b
  }
}

util.inherits(Sensor, EventEmitter)

Sensor.prototype.read = function() {}
Sensor.prototype.write = function() {}
Sensor.prototype.stream = function(delay, cb) {
  var self = this
  self.stopStream()
  streamInterval = setInterval(function onInterval() {
    var res = self.read()
    cb(res)
  }, delay)
}
Sensor.prototype.stopStream = function() {
  if (typeof streamInterval != 'undefined' && typeof streamInterval.clearInterval == 'function')
    streamInterval.clearInterval()
}
Sensor.prototype.watch = function(delay) {
  var self = this
  var delay = typeof delay == 'undefined' ? watchDelay : delay
  self.stopWatch()
  watchInterval = setInterval(function onInterval() {
    var res = self.read()

    self.lastValue = self.currentValue
    self.currentValue = res

    if (!isEqual(self.currentValue, self.lastValue))
      self.emit('change', self.currentValue)
  }, delay)
}
Sensor.prototype.stopWatch = function() {
  if (typeof watchInterval != 'undefined' && typeof watchInterval.clearInterval == 'function')
    watchInterval.clearInterval()
}

module.exports = Sensor