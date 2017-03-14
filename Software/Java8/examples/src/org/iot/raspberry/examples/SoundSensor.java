package org.iot.raspberry.examples;

import java.io.IOException;
import org.iot.raspberry.grovepi.GroveDigitalOut;
import org.iot.raspberry.grovepi.GrovePi;
import org.iot.raspberry.grovepi.devices.GroveSoundSensor;

/*
 Connect:
 SoundSensor to A0
 Leds to D3 (red),D4 (green) and D5 (blue)
 */
public class SoundSensor implements Example {

  @Override
  public void run(GrovePi grovePi, Monitor monitor) throws Exception {
    GroveSoundSensor soundSensor = new GroveSoundSensor(grovePi, 0);
    GroveDigitalOut redLed = grovePi.getDigitalOut(3);
    GroveDigitalOut greenLed = grovePi.getDigitalOut(4);
    GroveDigitalOut blueLed = grovePi.getDigitalOut(5);
    GroveDigitalOut onLed = null;
    while (monitor.isRunning()) {
      try {
        double soundLevel = soundSensor.get();
        System.out.println(soundLevel);
        GroveDigitalOut ledToTurn;
        if (soundLevel > 1000) {
          ledToTurn = redLed;
        } else if (soundLevel < 300) {
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
