package org.iot.raspberry.grovepi.devices;

import java.io.IOException;
import org.iot.raspberry.grovepi.GroveDigitalPin;
import org.iot.raspberry.grovepi.GrovePi;
import static org.iot.raspberry.grovepi.GrovePiCommands.*;
import org.iot.raspberry.grovepi.GroveUtil;

@GroveDigitalPin
public class GroveUltrasonicRanger {

  private final GrovePi grovePi;
  private final int pin;

  public GroveUltrasonicRanger(GrovePi grovePi, int pin) {
    this.grovePi = grovePi;
    this.pin = pin;
  }

  public double get() throws IOException {
    return grovePi.exec((io) -> {
      io.write(uRead_cmd, pin, unused, unused);
      io.sleep(200);
      int[] v = GroveUtil.unsign(io.read(new byte[4]));
      return (v[1] * 256) + v[2];
    });
  }

}
