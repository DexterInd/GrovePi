package org.iot.raspberry.grovepi;

import java.util.ArrayList;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;

public class GroveDevices implements AutoCloseable {

  private final List<AutoCloseable> devices = new ArrayList<>();

  public <T extends AutoCloseable> T add(T device) {
    devices.add(device);
    return device;
  }

  @Override
  public void close() {
    devices.stream().forEach((device) -> {
      try {
        device.close();
      } catch (Exception ex) {
        Logger.getLogger("RaspberryPi").log(Level.SEVERE, null, ex);
      }
    });
  }

}
