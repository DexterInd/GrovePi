package org.iot.raspberry.grovepi.dio;

import java.io.IOException;
import java.util.logging.Level;
import java.util.logging.Logger;
import jdk.dio.DeviceManager;
import jdk.dio.i2cbus.I2CDevice;
import jdk.dio.i2cbus.I2CDeviceConfig;
import org.iot.raspberry.grovepi.GrovePiSequenceVoid;
import org.iot.raspberry.grovepi.devices.GroveRgbLcd;

public class GroveRgbLcdDIO extends GroveRgbLcd {

  private final I2CDevice rgb;
  private final I2CDevice text;

  public GroveRgbLcdDIO() throws IOException {
    final int i2cBus = 1;                        // Raspberry Pi's I2C bus
    final int serialClock = 3400000;             // 3.4MHz Max clock
    final int addressSizeBits = 7;               // Device address size in bits

    this.text = DeviceManager.open(new I2CDeviceConfig(i2cBus, DISPLAY_TEXT_ADDR, addressSizeBits, serialClock));

    this.rgb = DeviceManager.open(new I2CDeviceConfig(i2cBus, DISPLAY_RGB_ADDR, addressSizeBits, serialClock));

    init();
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

  @Override
  public void close() {
    try {
      rgb.close();
    } catch (IOException ex) {
      Logger.getLogger("GrovePi").log(Level.SEVERE, null, ex);
    }
    try {
      text.close();
    } catch (IOException ex) {
      Logger.getLogger("GrovePi").log(Level.SEVERE, null, ex);
    }
  }

}
