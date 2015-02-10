GrovePi for Node.js
=======

GrovePi is an open source platform for connecting Grove Sensors to the Raspberry Pi.

These files have been made available online through a [Creative Commons Attribution-ShareAlike 3.0](http://creativecommons.org/licenses/by-sa/3.0/) license.

## Table of contents

- [Quick start](#quick-start)
- [Conclusions](#conclusions)

## Quick start

Before to start you should install Node.js on your RaspberryPi and clone the repo on your local environment. 
Be sure to have npm installed and then you can proceed installing the package.

Go inside your Node.js application folder and type
```bash
$ npm install node-grovepi
```
Now you can include the module inside your application as usual:
```javascript
var grovepi = require('node-grovepi')
```

Once the module has been loaded you can start using it in two ways:
### Single read
```javascript
grovepi.init({
  onInit: function callback() {
    grovepi.version(function onVersion(res) {
      console.log('Version')
      console.log(res)
    });
  },
  onError: function(err) {
    console.log(err)
  }
});
```
This method is useful if you don't need to perform several readings in a (very really) short period of time.
Actually, I faced issues due to concurrent access to the board, so be careful following this method.

### Waterfall readings
```javascript
grovepi.init({
  onInit: function callback() {
    grovepi.run([
      function(callback) {
        grovepi.version(function onVersion(res) {
          console.log('Version')
          console.log(res)
          callback()
        });
      },
      function(callback) {
        grovepi.light(SENSOR_PORT_NUMBER, function onLight(res) {
          console.log('Light')
          console.log(res)
          callback()
        });
      }
    ]);
  },
  onError: function(err) {
    console.log(err)
  }
});
```
Even if it could seems to be a bit messy, this method is perfect if you need to execute more than one reading in a short period of time;
It executes a list of tasks only when the previous one has been completed, this ensure to avoid any concurrent request.

## Conclusions
A lot of improvements are waiting to be implemented so be patient and stay focused! :-)