package org.iot.raspberry.grovepi.pi4j;

import com.pi4j.io.i2c.I2CBus;
import com.pi4j.io.i2c.I2CDevice;
import com.pi4j.io.i2c.I2CFactory;
import java.io.IOException;
import java.util.logging.Level;
import java.util.logging.Logger;
import org.iot.raspberry.grovepi.GrovePi;
import org.iot.raspberry.grovepi.GrovePiSequence;
import org.iot.raspberry.grovepi.GrovePiSequenceVoid;
import org.iot.raspberry.grovepi.devices.GroveRgbLcd;

/**
 * Create a new GrovePi interface using the Pi4j library
 *
 * @author Eduardo Moranchel <emoranchel@asmatron.org>
 */
public class GrovePi4J implements GrovePi {

  private static final int GROVEPI_ADDRESS = 4;
  private final I2CBus bus;
  private final I2CDevice device;

  public GrovePi4J() throws IOException {
    this.bus = I2CFactory.getInstance(I2CBus.BUS_1);
    this.device = bus.getDevice(GROVEPI_ADDRESS);
  }

  @Override
  public <T> T exec(GrovePiSequence<T> sequence) throws IOException {
    synchronized (this) {
      return sequence.execute(new IO(device));
    }
  }

  @Override
  public void execVoid(GrovePiSequenceVoid sequence) throws IOException {
    synchronized (this) {
      sequence.execute(new IO(device));
    }
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
  public GroveRgbLcd getLCD() throws IOException {
    return new GroveRgbLcdPi4J();
  }
}
