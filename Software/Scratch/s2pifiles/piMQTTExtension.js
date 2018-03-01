// Modified piGPIOExtension.js for GrovePi
// Ver 2.01Mar18 
new (function() {
    var ext = this;
    var fs = require('fs');
    var websocket;
    var sensorSplit; 
    var sensorDict = {};
    var variableDict = {};
    var mqtt = require('mqtt');
    //var client  = mqtt.connect('ws://cycy42.ddns.net',{port:1884})
    var client; // mqtt.connect('mqtt://cycy42.ddns.net');
    
    //var client  = mqtt.connect('mqtt://test.mosquitto.org')
 
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
     


function processData(data)
{
    console.log(data.field1);
    var cols = {blue:'0000ff',pink:'ffc0cb',oldlace:'fdf5e6',warmwhite:'fdf5e6',red:'ff0000',green:'008000',white:'ffffff',cyan:'00ffff',purple:'800080',magenta:'ff00ff',yellow:'ffff00',orange:'ffa500'};
    sensorDict["cheerlights"] = data.field1;
    if (data.field1 in cols) {
        sensorDict["cheerlights_hex"] = cols[data.field1]
    }
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
        if (bmsg1 == "get_cheerlights") {
            $.ajax({
                type: "GET",
                url: "http://api.thingspeak.com/channels/1417/field/1/last.json",
                dataType: "json",
                success: processData,
                error: function(){ console.log("Cheerlights request failed"); }
            });
        }
        else {
            sendMessage('broadcast "' + bmsg1 + '"');
        }
    };

    ext.mqtt_connect = function (mqtt_broker)
    {
        client = mqtt.connect('mqtt://' + mqtt_broker);
        client.on('connect', function () {
            //client.subscribe('#')
            //client.publish('swpresence', 'Hello at:' + Date.now(),{retain : true,qos : 1})
            console.log('Connected');
        });
 
        client.on('message', function (topic, message) {
            // message is Buffer
            console.log(topic.toString());
            console.log(message.toString());
            sensorDict[topic.toString()] = message.toString();
            //client.end()
        });
    };

    
    ext.mqtt_publish = function (mqtt_topic, mqtt_message)
    {
        client.publish(mqtt_topic, mqtt_message,{retain : true,qos : 1});
        console.log('mqqt published');
    };
    
    ext.mqtt_subscribe = function (mqtt_topic)
    {
        client.subscribe(mqtt_topic);
        console.log('mqqt subscribed to ' + mqtt_topic);
    };

    ext.get_sensorMsgs = function (sensorName) 
    {
        if (sensorName.toLowerCase() == "?") {
            console.log(JSON.stringify(sensorDict));
            var allSensors = '';
            for (var key in sensorDict) {
                if (sensorDict.hasOwnProperty(key)) {
                    allSensors = allSensors + key + '\n';
                }
            };
            return allSensors;
        } else {
            console.log(sensorName.toLowerCase() + ':' + sensorDict[sensorName.toLowerCase()])
            return sensorDict[sensorName.toLowerCase()];
        }
    };


    
    // Block and block menu descriptions
    var descriptor = {
        blocks: [
            [' ', 'Connect: %s', 'mqtt_connect','cycy42.ddns.net'],
            [' ', 'Publish topic: %s msg: %s', 'mqtt_publish','',''],
            [' ', 'Subscribe topic: %s', 'mqtt_subscribe','#'],
            ['r', 'Topic: %s value', 'get_sensorMsgs', '']
 
 
        ],
        menus: {
            sensorvals: ['cheerlights','cheerlights_hex']

		}
    };

    // Register the extension
    ScratchExtensions.register('MQTT', descriptor, ext);
})();
