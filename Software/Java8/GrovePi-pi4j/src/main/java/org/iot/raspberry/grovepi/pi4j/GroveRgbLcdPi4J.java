package org.iot.raspberry.grovepi.pi4j;

import com.pi4j.io.i2c.I2CBus;
import com.pi4j.io.i2c.I2CDevice;
import com.pi4j.io.i2c.I2CFactory;
import java.io.IOException;
import java.util.logging.Level;
import java.util.logging.Logger;
import org.iot.raspberry.grovepi.GrovePiSequenceVoid;
import org.iot.raspberry.grovepi.devices.GroveRgbLcd;

public class GroveRgbLcdPi4J extends GroveRgbLcd {

  private final I2CBus bus;
  private final I2CDevice rgb;
  private final I2CDevice text;

  public GroveRgbLcdPi4J() throws IOException {
    this.bus = I2CFactory.getInstance(I2CBus.BUS_1);
    this.rgb = bus.getDevice(DISPLAY_RGB_ADDR);
    this.text = bus.getDevice(DISPLAY_TEXT_ADDR);
    init();
  }

  @Override
  public void close() {
    try {
      bus.close();
    } catch (IOException ex) {
      Logger.getLogger("GrovePi").log(Level.SEVERE, null, ex);
    }
  }

  @Override
  public void execRGB(GrovePiSequenceVoid sequence) throws IOException {
    synchronized (this) {
      sequence.execute(new IO(rgb));
    }
  }

  @Override
  public void execTEXT(GrovePiSequenceVoid sequence) throws IOException {
    synchronized (this) {
      sequence.execute(new IO(text));
    }
  }

}
