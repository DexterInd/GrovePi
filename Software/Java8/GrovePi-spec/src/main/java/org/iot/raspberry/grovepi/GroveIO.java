package org.iot.raspberry.grovepi;

import java.io.IOException;

public interface GroveIO {

  public void write(int... command) throws IOException;

  public int read() throws IOException;

  public byte[] read(byte[] buffer) throws IOException;

  default public void sleep(long millis) {
    try {
      Thread.sleep(millis);
    } catch (InterruptedException ex) {
    }
  }
}
