var DigitalInput = require('./base/digitalSensor')

const buttonMode = {
    UP: 0,
    DOWN: 1
}

let mode = buttonMode.UP //not pressed

let datetimePressed

//digital button, can throw singlepress and longpress events
function DigitalButton(pin, longpressDelay) {
    DigitalInput.apply(this, Array.prototype.slice.call(arguments))
    this.longpressDelay = longpressDelay || 1100
    this.on('change', function (res) {
        //user presses the button for the first time
        if (res == 1 && mode === buttonMode.UP) {
            mode = buttonMode.DOWN
            datetimePressed = new Date()
            return
        }
        //user continues to press the button
        else if (res == 1 && mode === buttonMode.DOWN) {
            //do nothing
            return
        } else { //res == 0 so user has lifted her finger
            let currentDateTime = new Date()
            let miliseconds = currentDateTime.getTime() - datetimePressed.getTime()
            //if less than longgpressDelay miliseconds
            if (miliseconds <= this.longpressDelay) {
                this.emit('down', 'singlepress')
            } else {
                this.emit('down', 'longpress')
            }
            //reset the mode
            mode = buttonMode.UP
        }
    });
}

DigitalButton.prototype = new DigitalInput()

module.exports = DigitalButton