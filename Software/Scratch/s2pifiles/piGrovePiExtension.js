// Modified piGPIOExtension.js for GrovePi
// Ver 2.25Feb18 
new (function() {
    var ext = this;
    var fs = require('fs');
    var websocket;
    var sensorSplit; 
    var sensorDict = {};
    var variableDict = {};


    function doConnect() 
    {
      websocket = new WebSocket('ws://localhost:8000/')
      websocket.onopen = function(evt) { onOpen(evt) }
      websocket.onclose = function(evt) { onClose(evt) }
      websocket.onmessage = function(evt) { onMessage(evt) }
      websocket.onerror = function(evt) { onError(evt) }
      console.log('websocket connected from piGrovePiExtension')
    }

    function onOpen(evt) {
      console.log('websocket opened')
    }

    function onClose(evt) {
      console.log('websocket closed')
    }

    function onMessage(evt) {
      var data = evt.data
      console.log('msg from sgh:' + data)
      sensorSplit = data.split(":");
      sensorDict[sensorSplit[0]] = sensorSplit[1];
      // console.log('sensorDict=' + JSON.stringify(sensorDict))
    }

    function onError(evt) {
      var error = evt.data
      console.log('websocket error', error);
      
      websocket.close();
    }

    function sendMessage(message) {
      websocket.send(message);
      console.log('msg to sgh:' + message)
    }

    function doDisconnect() {
      websocket.close();
     }
     


    doConnect();

    // Cleanup function when the extension is unloaded
    ext._shutdown = function ()
    {
        for (pin = 2; pin < 28; pin++)
        {
            if (fs.existsSync("/sys/class/gpio/gpio" + pin))
                fs.writeFileSync("/sys/class/gpio/unexport", pin, "utf8");
        }
    };

    // Status reporting code
    // Use this to report missing hardware, plugin or unsupported browser
    ext._getStatus = function ()
    {
        return {status: 2, msg: 'Ready'};
    };

    ext.set_gpio = function (pin, val) 
    {
        if (pin === '' || pin < 0 || pin > 27) return;

        var dir = 0, lev;
        if (val == 'output high') lev = 1;
        else if (val == 'output low') lev = 0;
        else dir = 1;

		// check the pin is exported
		if (!fs.existsSync("/sys/class/gpio/gpio" + pin)) 

			fs.writeFileSync("/sys/class/gpio/export", pin, "utf8");

		// the ownership of direction takes time to establish, so try this until it succeeds
		while (true)
		{
			try {
				fs.writeFileSync("/sys/class/gpio/gpio" + pin + "/direction", dir == 0 ? "out" : "in", "utf8");
				break;
			}
			catch (error) {
				continue;
			}
		}

		// set the output value
        if (dir == 0)
            sendMessage('pin ' + pin + ' = ' + (lev == 1 ? "1" : "0"));
            fs.writeFileSync("/sys/class/gpio/gpio" + pin + "/value", lev == 1 ? "1" : "0", "utf8");
    };
  
    ext.get_gpio = function (pin) 
    {
        if (pin === '' || pin < 0 || pin > 27) return;

		// check the pin is exported
		if (!fs.existsSync("/sys/class/gpio/gpio" + pin)) 
			fs.writeFileSync("/sys/class/gpio/export", pin);

		// read the pin value
		var data = fs.readFileSync ("/sys/class/gpio/gpio" + pin + "/value", 'utf8');

		if (data.slice(0,1) == "1") return true;
		else return false;
    };
    
//my code

    ext.send_broadcast1 = function (bmsg1 ,bmsg2) 
    {
        sendMessage('broadcast "' + bmsg1 + bmsg2 + '"');
    };

    ext.send_broadcast2 = function (bmsg1 ,bmsg2,bmsg3) 
    {
        sendMessage('broadcast "' + bmsg1 + bmsg2 + bmsg3 + '"');
    };
    
    ext.send_broadcast0 = function (bmsg1) 
    {
        sendMessage('broadcast "' + bmsg1 + '"');
    };

    ext.get_sensorMsgs = function (sensorName) 
    {
    console.log(sensorName.toLowerCase() + ':' + sensorDict[sensorName.toLowerCase()])
    //fs.writeFileSync("/home/pi/GrovePiSensors.json", JSON.stringify(sensorDict), "utf8");
    return sensorDict[sensorName.toLowerCase()];
    };

    
    // Block and block menu descriptions
    var descriptor = {
        blocks: [

            [' ', 'broadcast %m.broadcastType %s', 'send_broadcast1', 'digitalRead','0'],
            [' ', 'broadcast %m.broadcastType2 %m.ports %s', 'send_broadcast2', 'analogWrite','0','0'],
            [' ', 'broadcast %m.broadcastType0', 'send_broadcast0', 'take_picture'],
            ['r', '%m.sensorvals value', 'get_sensorMsgs', 'digitalread'],
 
 
        ],
        menus: {
            sensorvals: ['digitalread','analogread','moisture','light','sound','rotary','distance','temp','humidty','folder','camera'],
            broadcastType: ['digitalRead','analogRead','digitalWriteHigh','moisture','light','sound','rotary','distance','button','relay','temp','humidty','folder','take_picture','speak','lcdcol','lcdtxt'],
            broadcastType2: ['analogWrite','buzzer','led'],
            broadcastType0: ['take_picture'],
            ports: ['0','1','2','3','4','5','6','7']

		}
    };

    // Register the extension
    ScratchExtensions.register('GrovePi', descriptor, ext);
})();
