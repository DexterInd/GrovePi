package org.iot.raspberry.grovepi.devices;

import java.io.IOException;
import org.iot.raspberry.grovepi.GroveDigitalPin;
import org.iot.raspberry.grovepi.GroveIO;
import org.iot.raspberry.grovepi.GrovePi;
import static org.iot.raspberry.grovepi.GrovePiCommands.*;

@GroveDigitalPin
public class GroveLed {

  public static int MAX_BRIGTHNESS = 255;

  private final GrovePi grovePi;
  private final int pin;

  public GroveLed(GrovePi grovePi, int pin) throws IOException {
    this.grovePi = grovePi;
    this.pin = pin;
    grovePi.execVoid((GroveIO io) -> io.write(pMode_cmd, pin, pMode_out_arg, unused));
    set(false);
  }

  public final void set(boolean value) throws IOException {
    int val = value ? 1 : 0;
    grovePi.execVoid((GroveIO io) -> io.write(dWrite_cmd, pin, val, unused));
  }

  public final void set(int value) throws IOException {
    final int val = ((value > 255) ? 255 : (value < 0 ? 0 : value));
    grovePi.execVoid((GroveIO io) -> io.write(aWrite_cmd, pin, val, unused));
  }

}
