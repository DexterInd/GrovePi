package org.iot.raspberry.grovepi.devices;

import java.io.IOException;
import org.iot.raspberry.grovepi.GroveAnalogPin;
import org.iot.raspberry.grovepi.GrovePi;
import org.iot.raspberry.grovepi.GroveUtil;

@GroveAnalogPin
public class GroveRotarySensor extends GroveAnalogInputDevice<GroveRotaryValue> {

  //Reference voltage of ADC is 5v
  public static final double ADC_REF = 5;
  //Vcc of the grove interface is normally 5v
  public static final double GROVE_VCC = 5;
  //Full value of the rotary angle is 300 degrees, as per it's specs (0 to 300)
  public static final double FULL_ANGLE = 300;

  public GroveRotarySensor(GrovePi grovePi, int pin) throws IOException {
    super(grovePi.getAnalogIn(pin, 4));
  }

  @Override
  public GroveRotaryValue get(byte[] b) {
    int[] v = GroveUtil.unsign(b);
    double sensor_value = (v[1] * 256) + v[2];
    double voltage = (sensor_value * ADC_REF / 1023);
    double degrees = voltage * FULL_ANGLE / GROVE_VCC;
    return new GroveRotaryValue(sensor_value, voltage, degrees);
  }

}
