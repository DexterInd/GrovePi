package org.iot.raspberry.examples;

import java.io.IOException;
import org.iot.raspberry.grovepi.GrovePi;
import org.iot.raspberry.grovepi.devices.GroveTemperatureAndHumiditySensor;
/*
 Connect Temp & Humidity sensor to D4
 */

public class TemperatureAndHumidity implements Example {

  @Override
  public void run(GrovePi grovePi, Monitor monitor) throws Exception {
    GroveTemperatureAndHumiditySensor dht = new GroveTemperatureAndHumiditySensor(grovePi, 4, GroveTemperatureAndHumiditySensor.Type.DHT11);
    while (monitor.isRunning()) {
      try {
        System.out.println(dht.get());
      } catch (IOException ex) {
      }
    }
  }
}
