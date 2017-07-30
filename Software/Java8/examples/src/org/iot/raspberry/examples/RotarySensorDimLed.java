package org.iot.raspberry.examples;

import java.io.IOException;
import org.iot.raspberry.grovepi.GrovePi;
import org.iot.raspberry.grovepi.devices.GroveLed;
import org.iot.raspberry.grovepi.devices.GroveRotarySensor;
import org.iot.raspberry.grovepi.devices.GroveRotaryValue;
/*
 Connect:
 RotarySensor to A1
 Led D5
 */

public class RotarySensorDimLed implements Example {

  @Override
  public void run(GrovePi grovePi, Monitor monitor) throws Exception {
    GroveRotarySensor rotarySensor = new GroveRotarySensor(grovePi, 1);
    GroveLed blueLed = new GroveLed(grovePi, 5);
    while (monitor.isRunning()) {
      try {
        GroveRotaryValue value = rotarySensor.get();
        int brightness = (int) (value.getFactor() * GroveLed.MAX_BRIGTHNESS);
        blueLed.set(brightness);
      } catch (IOException ex) {
        System.out.println("Error");
      }
    }
    blueLed.set(false);
  }

}
