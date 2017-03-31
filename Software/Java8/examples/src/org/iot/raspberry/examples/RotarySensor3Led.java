package org.iot.raspberry.examples;

import java.io.IOException;
import org.iot.raspberry.grovepi.GroveDigitalOut;
import org.iot.raspberry.grovepi.GrovePi;
import org.iot.raspberry.grovepi.devices.GroveRotarySensor;
import org.iot.raspberry.grovepi.devices.GroveRotaryValue;

/*
 Connect:
 RotarySensor to A1
 Leds to D3 (red),D4 (green) and D5 (blue)
 */
public class RotarySensor3Led implements Example {

  @Override
  public void run(GrovePi grovePi, Monitor monitor) throws Exception {
    GroveRotarySensor rotarySensor = new GroveRotarySensor(grovePi, 1);
    GroveDigitalOut redLed = grovePi.getDigitalOut(3);
    GroveDigitalOut greenLed = grovePi.getDigitalOut(4);
    GroveDigitalOut blueLed = grovePi.getDigitalOut(5);
    GroveDigitalOut onLed = null;
    while (monitor.isRunning()) {
      try {
        GroveRotaryValue value = rotarySensor.get();
        System.out.println(value);
        GroveDigitalOut ledToTurn;
        if (value.getDegrees() > 250) {
          ledToTurn = redLed;
        } else if (value.getDegrees() < 100) {
          ledToTurn = blueLed;
        } else {
          ledToTurn = greenLed;
        }
        if (ledToTurn != onLed) {
          redLed.set(ledToTurn == redLed);
          blueLed.set(ledToTurn == blueLed);
          greenLed.set(ledToTurn == greenLed);
          onLed = ledToTurn;
        }
      } catch (IOException ex) {
        System.out.println("Error");
      }
    }
    blueLed.set(false);
    greenLed.set(false);
    redLed.set(false);
  }

}
