// Modules
var i2c         = require('i2c-bus')
var async       = require('async')
var log         = require('npmlog')
var sleep       = require('sleep')
var fs          = require('fs')
var bufferTools = require('buffertools').extend()
var commands    = require('./commands')

var I2CCMD    = 1
var debugMode = false
var i2c0Path  = '/dev/i2c-0'
var i2c1Path  = '/dev/i2c-1'
var bus
var busNumber

var initWait  = 1     // in seconds

var isInit    = false
var isHalt    = false
var isBusy    = false

var ADDRESS   = 0x04

var onError, onInit

function GrovePi(opts) {
  this.BYTESLEN = 4
  this.INPUT = 'input'
  this.OUTPUT = 'output'

  if (typeof opts == 'undefined')
    opts = {}

  if (typeof opts.debug != 'undefined')
    this.debugMode = opts.debug
  else
    this.debugMode = debugMode

  // TODO: Dispatch an error event instead
  if (typeof opts.onError == 'function')
    onError = opts.onError

  // TODO: Dispatch a init event instead
  if (typeof opts.onInit == 'function')
    onInit = opts.onInit

  if (fs.existsSync(i2c0Path)) {
    isHalt = false
    busNumber = 0
  } else if (fs.existsSync(i2c1Path)) {
    isHalt = false
    busNumber = 1
  } else {
    var err = new Error('GrovePI could not determine your i2c device')
    isHalt = true
    if (typeof onError == 'function')
      onError(err)
    this.debug(err)
  }
}

GrovePi.prototype.init = function() {
  if (!isHalt) {
    bus = i2c.openSync(busNumber)

    if (!isInit) {
      this.debug('GrovePi is initing')
      sleep.sleep(initWait)
      isInit = true

      if (typeof onInit == 'function')
        onInit(true)
    } else {
      var err = new Error('GrovePI is already initialized')
      if (typeof onInit == 'function')
        onInit(false)
      onError(err)
    }
  } else {
    var err = new Error('GrovePI cannot be initialized')
    if (typeof onInit == 'function')
      onInit(false)
    onError(err)
  }
}
GrovePi.prototype.close = function() {
  if (typeof bus != 'undefined') {
    this.debug('GrovePi is closing')
    bus.closeSync()
  } else {
    this.debug('The device is not defined')
  }
}
GrovePi.prototype.run = function(tasks) {
  this.debug('GrovePi is about to execute ' + tasks.length + ' tasks')
  async.waterfall(tasks)
}
GrovePi.prototype.checkStatus = function() {
  if (!isInit || isHalt){
    if (!isHalt) {
      this.debug('GrovePi needs to be initialized.')
    } else {
      this.debug('GrovePi is not operative because halted')
    }
    return false
  }
  return true
}
GrovePi.prototype.readByte = function() {
  var isOperative = this.checkStatus()
  if (!isOperative)
    return false

  var length = 1
  var buffer = new Buffer(length)
  var ret = bus.i2cReadSync(ADDRESS, length, buffer)
  return ret > 0 ? buffer : false
}
GrovePi.prototype.readBytes = function(length) {
  if (typeof length == 'undefined')
    length = this.BYTESLEN

  var isOperative = this.checkStatus()
  if (!isOperative)
    return false

  var buffer = new Buffer(length)
  var ret = false
  try {
    var val = bus.i2cReadSync(ADDRESS, length, buffer)
    ret = val > 0 ? buffer : false
  } catch (err) {
    ret = false
  } finally {
    return ret
  }
}
GrovePi.prototype.writeBytes = function(bytes) {
  var isOperative = this.checkStatus()
  if (!isOperative)
    return false

  var buffer = new Buffer(bytes)
  var ret = false
  try {
    var val = bus.i2cWriteSync(ADDRESS, buffer.length, buffer)
    ret = val > 0 ? true : false
  } catch (err) {
    ret = false
  } finally {
    return ret
  }
}
GrovePi.prototype.pinMode = function(pin, mode) {
  var isOperative = this.checkStatus()
  if (!isOperative)
    return false

  if (mode == this.OUTPUT) {
    return this.writeBytes(commands.pMode.concat([pin, 1, commands.unused]))
  } else if (mode == this.INPUT) {
    return this.writeBytes(commands.pMode.concat([pin, 0, commands.unused]))
  } else {
    this.debug('Unknown pin mode')
  }
}
GrovePi.prototype.debug = function(msg) {
  if (this.debugMode)
    log.info('GrovePi.board', msg)
}
GrovePi.prototype.wait = function(ms) {
  sleep.usleep(1000 * ms)
}

// GrovePi functions
GrovePi.prototype.version = function() {
  var write = this.writeBytes(commands.version.concat([commands.unused, commands.unused, commands.unused]))
  if (write) {
    this.wait(100)
    this.readByte()
    var bytes = this.readBytes()
    if (typeof bytes == 'object')
      return (bytes[1] + '.' + bytes[2] + '.' + bytes[3])
    else
      return false
  } else {
    return false
  }
}

// export the class
module.exports = GrovePi
