package com.dexterind.grovepi;

import java.io.IOException;
import java.io.PrintWriter;
import java.io.StringWriter;
import java.nio.ByteBuffer;
import java.util.*;

import com.dexterind.grovepi.*;
import com.dexterind.grovepi.events.*;
import com.dexterind.grovepi.utils.*;

import com.pi4j.io.i2c.I2CBus;
import com.pi4j.io.i2c.I2CDevice;
import com.pi4j.io.i2c.I2CFactory;
import com.pi4j.system.NetworkInfo;
import com.pi4j.system.SystemInfo;

public class Board {

  private static Board instance = null;
  private final I2CDevice device;

  public static final byte PIN_MODE_OUTPUT = 1;
  public static final byte PIN_MODE_INPUT = 0;
  private static final byte ADDRESS = 0x04;
  
  private Debug debug;

  public Board() throws IOException, InterruptedException, Exception {
    int busId;

    String type = SystemInfo.getBoardType().name();

    if (type.indexOf("ModelA") > 0) {
      busId = I2CBus.BUS_0;
    } else {
      busId = I2CBus.BUS_1;
    }

    final I2CBus bus = I2CFactory.getInstance(busId);
    device = bus.getDevice(ADDRESS);
  }

  public static Board getInstance() throws IOException, InterruptedException, Exception {
    if(instance == null) {
      instance = new Board();
    }
    return instance;
  }

  public int writeI2c(int... bytes) throws IOException {
    // Convert array: int[] to byte[]
    final ByteBuffer byteBuffer = ByteBuffer.allocate(bytes.length);
    for (int i = 0, len = bytes.length; i < len; i++) {
      byteBuffer.put((byte) bytes[i]);
    }
    sleep(100);
    device.write(0xfe, byteBuffer.array(), 0, byteBuffer.limit());
    return Statuses.OK;
  }

  public byte[] readI2c(int numberOfBytes) throws IOException {
    byte[] buffer = new byte[numberOfBytes];
    device.read(1, buffer, 0, buffer.length);
    return buffer;
  }

  public int setPinMode(int pin, int pinMode) throws IOException {
    return writeI2c(Commands.PMODE, pin, pinMode, Commands.UNUSED);
  }

  public void sleep(int msec) {
    try {
      Thread.sleep(msec);
    } catch (InterruptedException e) {
      throw new IllegalStateException(e);
    }
  }

  public void init() {
    try {
      device.write(0xfe, (byte)0x04);
    } catch (IOException e) {
      StringWriter sw = new StringWriter();
      e.printStackTrace(new PrintWriter(sw));
      String exceptionDetails = sw.toString();
      debug.log(Debug.SEVERE, exceptionDetails);
    }
  }

  public String version() throws IOException {
    writeI2c(Commands.VERSION, Commands.UNUSED, Commands.UNUSED, Commands.UNUSED);
    sleep(100);

    byte[] b = readI2c(4);
    readI2c(1);
    
    return String.format("%s.%s.%s", (int)b[1], (int)b[2], (int)b[3]);
  }

}
