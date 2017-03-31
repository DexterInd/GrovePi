package org.iot.raspberry.grovepi.devices;

import java.io.IOException;
import org.iot.raspberry.grovepi.GroveAnalogPin;
import org.iot.raspberry.grovepi.GrovePi;
import org.iot.raspberry.grovepi.GroveUtil;

@GroveAnalogPin
public class GroveSoundSensor extends GroveAnalogInputDevice<Double> {

  public GroveSoundSensor(GrovePi grovePi, int pin) throws IOException {
    super(grovePi.getAnalogIn(pin, 4));
  }

  @Override
  public Double get(byte[] b) {
    int[] v = GroveUtil.unsign(b);
    return (double) (v[1] * 256) + v[2];
  }
}
