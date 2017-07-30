package org.iot.raspberry.grovepi;

import java.io.IOException;
import static org.iot.raspberry.grovepi.GrovePiCommands.*;

public class GroveDigitalOut {

  private final GrovePi grovePi;
  private final int pin;

  public GroveDigitalOut(GrovePi grovePi, int pin) throws IOException {
    this.grovePi = grovePi;
    this.pin = pin;
    grovePi.execVoid((GroveIO io) -> io.write(pMode_cmd, pin, pMode_out_arg, unused));
    set(false);
  }

  public final void set(boolean value) throws IOException {
    int val = value ? 1 : 0;
    grovePi.execVoid((GroveIO io) -> io.write(dWrite_cmd, pin, val, unused));
  }
}
