package org.iot.raspberry.grovepi.dio;

import java.io.IOException;
import jdk.dio.DeviceManager;
import jdk.dio.i2cbus.I2CDevice;
import jdk.dio.i2cbus.I2CDeviceConfig;
import org.iot.raspberry.grovepi.GrovePi;
import org.iot.raspberry.grovepi.GrovePiSequence;
import org.iot.raspberry.grovepi.GrovePiSequenceVoid;
import org.iot.raspberry.grovepi.devices.GroveRgbLcd;

/**
 * Create a new GrovePi interface using the Device I/O
 *
 * @author Eduardo Moranchel <emoranchel@asmatron.org>
 */
public class GrovePiDio implements GrovePi {

  private final I2CDevice device;

  public GrovePiDio() throws IOException {
    final int i2cBus = 1;                        // Raspberry Pi's I2C bus
    final int address = 0x04;                    // Device address
    final int serialClock = 3400000;             // 3.4MHz Max clock
    final int addressSizeBits = 7;               // Device address size in bits

    I2CDeviceConfig config = new I2CDeviceConfig(i2cBus, address, addressSizeBits, serialClock);
    device = DeviceManager.open(config);

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
  }

  @Override
  public GroveRgbLcd getLCD() throws IOException {
    return new GroveRgbLcdDIO();
  }

}
