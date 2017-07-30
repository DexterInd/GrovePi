package org.iot.raspberry.examples;

import java.io.IOException;
import org.iot.raspberry.grovepi.GroveDigitalOut;
import org.iot.raspberry.grovepi.GrovePi;
import org.iot.raspberry.grovepi.devices.GroveUltrasonicRanger;

/*
 Connect ultrasonic ranger to port D6
 buzzer to D7
 */

public class UltrasonicRanger implements Example {

  @Override
  public void run(GrovePi grovePi, Monitor monitor) throws Exception {
    GroveUltrasonicRanger ranger = new GroveUltrasonicRanger(grovePi, 6);
    GroveDigitalOut buzzer = grovePi.getDigitalOut(7);
    while (monitor.isRunning()) {
      try {
        double distance = ranger.get();
        System.out.println(distance);
        buzzer.set(distance < 20);
      } catch (IOException ex) {
        System.out.println("error!");
      }
    }
  }

}
