package org.iot.raspberry.grovepi;

import org.iot.raspberry.grovepi.devices.GroveRgbLcd;
import java.io.IOException;

public interface GrovePi extends AutoCloseable {

  default public GroveDigitalOut getDigitalOut(int digitalPort) throws IOException {
    return new GroveDigitalOut(this, digitalPort);
  }

  default public GroveDigitalIn getDigitalIn(int digitalPort) throws IOException {
    return new GroveDigitalIn(this, digitalPort);
  }

  default public GroveAnalogOut getAnalogOut(int digitalPort) throws IOException {
    return new GroveAnalogOut(this, digitalPort);
  }

  default public GroveAnalogIn getAnalogIn(int digitalPort, int bufferSize) throws IOException {
    return new GroveAnalogIn(this, digitalPort, bufferSize);
  }

  public GroveRgbLcd getLCD() throws IOException;

  public <T> T exec(GrovePiSequence<T> sequence) throws IOException;

  public void execVoid(GrovePiSequenceVoid sequence) throws IOException;

  @Override
  public void close();

}
