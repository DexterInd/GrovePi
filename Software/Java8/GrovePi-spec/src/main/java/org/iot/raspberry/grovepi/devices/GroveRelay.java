package org.iot.raspberry.grovepi.devices;

import java.io.IOException;
import org.iot.raspberry.grovepi.GroveDigitalPin;
import org.iot.raspberry.grovepi.GroveIO;
import org.iot.raspberry.grovepi.GrovePi;
import static org.iot.raspberry.grovepi.GrovePiCommands.dWrite_cmd;
import static org.iot.raspberry.grovepi.GrovePiCommands.pMode_cmd;
import static org.iot.raspberry.grovepi.GrovePiCommands.pMode_out_arg;
import static org.iot.raspberry.grovepi.GrovePiCommands.unused;

@GroveDigitalPin
public class GroveRelay {

  private final GrovePi grovePi;
  private final int pin;

  public GroveRelay(GrovePi grovePi, int pin) throws IOException {
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
