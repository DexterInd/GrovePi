/*
 * Class definition to interact with the Grove Accelerometer
 * Datasheet: http://wiki.seeedstudio.com/wiki/Grove_-_3-Axis_Digital_Accelerometer_ADXL345
 * 
 * I2C Definition - https://en.wikipedia.org/wiki/I%C2%B2C
 *
 * ARBITRATION ON I2C - 
 * Although conceptually a single-master bus, a slave device that supports the "host notify protocol" acts as a master to perform the notification. 
 * It seizes the bus and writes a 3-byte message to the reserved "SMBus Host" address (0x08), passing its address and two bytes of data. When two 
 * slaves try to notify the host at the same time, one of them will lose arbitration and need to retry.  
 * 
 * An alternative slave notification system uses the separate SMBALERT# signal to request attention. In this case, the host performs a 1-byte read 
 * from the reserved "SMBus Alert Response Address" (0x0c), which is a kind of broadcast address. All alerting slaves respond with a data bytes 
 * containing their own address. When the slave successfully transmits its own address (winning arbitration against others) it stops raising that interrupt. 
 * In both this and the preceding case, arbitration ensures that one slave's message will be received, and the others will know they must retry.
 * 
 * Class definition to interact with the Grove LCD RGB Display
 * 
 * @Author: Salvatore Castro (Among others; URL references are in comments)
 * @Date: February 20,2017
 */

'use strict';
const DigitalSensor = require('./base/digitalSensor');
const commands      = require('../commands');
const util          = require('util');
const EventEmitter  = require('events').EventEmitter;
const sleep         = require('sleep');
const math          = require('mathjs');

// Code is adapted from the python in the document
//ADXL345 constants
var _EARTH_GRAVITY_MS2 = 9.80665;  // varies depending on altitue and location
var _SCALE_MULTIPLIER  = 0.004;

const ACCELEROMETER_DATA_ADDR  = 0x53;
var _DATA_FORMAT       = 0x31;
var _BW_RATE           = 0x2C;
var _POWER_CTL         = 0x2D;

var _BW_RATE_1600HZ    = 0x0F;
var _BW_RATE_800HZ     = 0x0E; // Default
var _BW_RATE_400HZ     = 0x0D; 
var _BW_RATE_200HZ     = 0x0C;
var _BW_RATE_100HZ     = 0x0B; 
var _BW_RATE_50HZ      = 0x0A;
var _BW_RATE_25HZ      = 0x09;

var _RANGE_16G         = 0x03;

var _MEASURE           = 0x08;
var _AXES_DATA         = 0x32;

var _i2c    = null;
var _GForce = false;

var _lastValue    = 0;
var _currentValue = 0;
var _streamInterval = null;
var _watchInterval  = null;
var _watchDelay   = 250;

/**
 * Constructor 
 * @param i2c2	I2C Comm port display is connected on
 */
 var GroveAccelerometer = class GroveLCDRGBDisplay {
	constructor(i2c, gForce) {
		//DigitalSensor.apply(this, Array.prototype.slice.call(arguments));
		util.inherits(GroveAccelerometer, EventEmitter);
		this._i2c    = i2c;
		this._GForce = gForce;
		//console.log("GForce - Set: "+gForce+"  _GForce: "+this._GForce);
		//console.log("I2C - Set: "+i2c+"  _i2c: "+this._i2c);
		this.enableMeasurement();
		this.setBandwidthRate(_BW_RATE_800HZ);
		this.setRange(_RANGE_16G);
		this._lastValue    = 0;
		this._currentValue = 0;
		this._watchDelay   = 250;
		var _streamInterval = null;
		var _watchInterval  = null;
	}

	echo(input) {
		console.log("Echo: "+input);
		return input;
	}

	/**
	 * Turn on the device
	 */
	enableMeasurement() {	
		this._i2c.writeByteSync(ACCELEROMETER_DATA_ADDR, _POWER_CTL, _MEASURE);
	}

	/**
	 * Setup the interface speed
	 */
	setBandwidthRate(rate_flag) {
		this._i2c.writeByteSync(ACCELEROMETER_DATA_ADDR, _BW_RATE, rate_flag);
	}

	/**
	 * Tell the device which range you're expecting - 16g
	 */
	setRange(range_flag) {
		var value = this._i2c.readByteSync(ACCELEROMETER_DATA_ADDR, _DATA_FORMAT);
		//console.log("Range: "+value);
		value &= ~0x0F;
		value |= range_flag;
		value |= 0x08;
		//console.log("Acc.setRange: "+value);
		
		this._i2c.writeByteSync(ACCELEROMETER_DATA_ADDR, _DATA_FORMAT, value);
	}
 }

	/**
	 * Get the readings from the Accelerometer
	 * 	False (default): result is returned in m/s^2
	 * 	True           : result is returned in gs
	 * 
	 * @param	gForce	(boolean) See above description
	 * @returns	value from the sensor
	 */
GroveAccelerometer.prototype.read = function() {
	var bytes = this._i2c.readSync(ACCELEROMETER_DATA_ADDR, _AXES_DATA, 6);
	var x = bytes[0] | (bytes[1] << 8);
	if(x & (1 << 16 - 1)) {
		x = x - (1<<16);
	}

	var y = bytes[2] | (bytes[3] << 8);
	if(y & (1 << 16 - 1)) {
		y = y - (1<<16)
	}

	var z = bytes[4] | (bytes[5] << 8);
	if(z & (1 << 16 - 1)) {
		z = z - (1<<16);
	}

	x = x * _SCALE_MULTIPLIER;
	y = y * _SCALE_MULTIPLIER;
	z = z * _SCALE_MULTIPLIER;
//console.log(" !_GForce: "+(!this._GForce));
	if(!this._GForce) {
		x = x * _EARTH_GRAVITY_MS2;
		y = y * _EARTH_GRAVITY_MS2;
		z = z * _EARTH_GRAVITY_MS2;
	}
	var rms = math.round(math.sqrt((math.pow(x,2) + math.pow(y,2) + math.pow(z,2))), 5);
//console.log("  Accel - "+[x,y,z,rms]);

	x = (x).toFixed(5);
	y = (y).toFixed(5);
	z = (z).toFixed(5);

	return [x,y,z,rms];
}

	/**
	 * Delay to wait before reading, from /bin/libs/sensors/base/sensor.js
	 * 
	 * @param	delay	duration in milliseconds to wait
	 */
GroveAccelerometer.prototype.watch = function(delay) {
  var self = this;
  delay = typeof delay == 'undefined' ? self._watchDelay : delay;

  self.stopWatch();
  self._watchInterval = setInterval(function onInterval() {
    var res = self.read();

    self._lastValue = self._currentValue;
    self._currentValue = res;

    if (!isEqual(self._currentValue, self._lastValue))
      self.emit('change', self._currentValue);
  }, delay);
}
GroveAccelerometer.prototype.stopWatch = function() {
  var self = this;
  if (typeof self._watchInterval != 'undefined');
    clearInterval(self._watchInterval);
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

module.exports = GroveAccelerometer;
