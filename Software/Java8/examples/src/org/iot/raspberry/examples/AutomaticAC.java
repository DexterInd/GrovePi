package org.iot.raspberry.examples;

import java.io.IOException;
import org.iot.raspberry.grovepi.GroveDigitalOut;
import org.iot.raspberry.grovepi.GrovePi;
import org.iot.raspberry.grovepi.devices.GroveRelay;
import org.iot.raspberry.grovepi.devices.GroveRgbLcd;
import org.iot.raspberry.grovepi.devices.GroveTemperatureAndHumiditySensor;
import org.iot.raspberry.grovepi.devices.GroveTemperatureAndHumidityValue;
import org.iot.raspberry.grovepi.devices.GroveUltrasonicRanger;

/**
 * Connect:
 * Digital 3 -> Red led
 * Digital 4 -> Green led
 * Digital 5 -> blue led
 * Digital 6 -> Ultrasonic ranger
 * Digital 7 -> TemperatureSensor DHT11
 * Digital 8 -> Relay
 * Any I2C -> LCD
 * @author Eduardo Moranchel <emoranchel@asmatron.org>
 */
public class AutomaticAC implements Example {

  @Override
  public void run(GrovePi grovePi, Monitor monitor) throws Exception {
    GroveDigitalOut redLed = grovePi.getDigitalOut(3);
    GroveDigitalOut greenLed = grovePi.getDigitalOut(4);
    GroveDigitalOut blueLed = grovePi.getDigitalOut(5);
    GroveUltrasonicRanger ranger = new GroveUltrasonicRanger(grovePi, 6);
    GroveTemperatureAndHumiditySensor tempSensor = new GroveTemperatureAndHumiditySensor(grovePi, 7, GroveTemperatureAndHumiditySensor.Type.DHT11);
    GroveRelay relay = new GroveRelay(grovePi, 8);
    GroveRgbLcd lcd = grovePi.getLCD();
    while (monitor.isRunning()) {
      try {
        GroveTemperatureAndHumidityValue dht = tempSensor.get();
        double temperature = dht.getTemperature();
        double distance = ranger.get();
        String message = String.format("TEMP:%.2f\nDistance%.2f", temperature, distance);
        System.out.println(message);
        lcd.setText(message);
        if (temperature > 28) {
          if (distance < 50) {
            relay.set(true);
          } else {
            relay.set(false);
          }
          lcd.setRGB(255, 50, 50);
          redLed.set(true);
          blueLed.set(false);
          greenLed.set(false);
        } else if (temperature < 17) {
          relay.set(false);
          blueLed.set(true);
          redLed.set(false);
          greenLed.set(false);
          lcd.setRGB(50, 50, 255);
        } else {
          relay.set(false);
          blueLed.set(false);
          greenLed.set(true);
          lcd.setRGB(50, 255, 50);
        }
      } catch (IOException ioex) {
        System.out.println("Error");
      }
    }
    redLed.set(false);
    greenLed.set(false);
    blueLed.set(false);
    relay.set(false);
  }
}
