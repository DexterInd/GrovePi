package org.iot.raspberry.grovepi.dio;

import java.io.IOException;
import java.nio.ByteBuffer;
import java.util.Arrays;
import java.util.logging.Level;
import java.util.logging.Logger;
import jdk.dio.i2cbus.I2CDevice;
import org.iot.raspberry.grovepi.GroveIO;

public class IO implements GroveIO {

  private final I2CDevice device;

  public IO(I2CDevice device) {
    this.device = device;
  }

  // IO
  @Override
  public void write(int... cmd) throws IOException {
    ByteBuffer command = ByteBuffer.allocateDirect(cmd.length);
    Arrays.stream(cmd).forEach((c) -> command.put((byte) c));
    command.rewind();
    Logger.getLogger("GrovePi").log(Level.INFO, "[DIO IO write]{0}", Arrays.toString(cmd));
    device.write(command);
  }

  @Override
  public int read() throws IOException {
    final int read = device.read();
    Logger.getLogger("GrovePi").log(Level.INFO, "[DIO IO read]{0}", read);
    return read;
  }

  @Override
  public byte[] read(byte[] buffer) throws IOException {
    ByteBuffer bf = ByteBuffer.wrap(buffer);
    bf.rewind();
    device.read(bf);
    Logger.getLogger("GrovePi").log(Level.INFO, "[DIO IO read]{0}", buffer);
    return buffer;
  }

}
