package org.iot.raspberry.examples;

import java.io.IOException;
import org.iot.raspberry.grovepi.GroveDigitalOut;
import org.iot.raspberry.grovepi.GrovePi;
import org.iot.raspberry.grovepi.devices.GroveLightSensor;
/*
 Connect Light sensor to A2
 Connect Red Led to D3 (emergency Light)
 */

public class LightSensor implements Example {

  @Override
  public void run(GrovePi grovePi, Monitor monitor) throws Exception {
    GroveLightSensor lightSensor = new GroveLightSensor(grovePi, 2);
    GroveDigitalOut emergencyLight = new GroveDigitalOut(grovePi, 3);
    while (monitor.isRunning()) {
      try {
        Double value = lightSensor.get();
        emergencyLight.set(value < 250);
        System.out.println(value);
      } catch (IOException ex) {
        System.out.println("error");
      }
    }
    emergencyLight.set(false);
  }

}
