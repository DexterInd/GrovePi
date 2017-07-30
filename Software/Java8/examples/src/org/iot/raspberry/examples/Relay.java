/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package org.iot.raspberry.examples;

import java.io.IOException;
import org.iot.raspberry.grovepi.GrovePi;
import org.iot.raspberry.grovepi.devices.GroveRelay;

/*
 * Connect Relay to D8
 */
public class Relay implements Example {

  @Override
  public void run(GrovePi grovePi, Monitor monitor) throws Exception {
    GroveRelay relay = new GroveRelay(grovePi, 8);
    while (monitor.isRunning()) {
      try {
        relay.set(true);
        Thread.sleep(10000);
        relay.set(false);
        Thread.sleep(5000);
      } catch (IOException io) {
        System.err.println("error");
      }
    }
    relay.set(false);
  }

}
