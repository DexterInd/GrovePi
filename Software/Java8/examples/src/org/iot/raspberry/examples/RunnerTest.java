package org.iot.raspberry.examples;

import org.iot.raspberry.grovepi.GrovePi;

public class RunnerTest implements Example {

  @Override
  public void run(GrovePi grovePi, Monitor monitor) throws Exception {
    while (monitor.isRunning()) {
      Thread.sleep(1000);
      System.out.println("Running...");
    }
  }
}
