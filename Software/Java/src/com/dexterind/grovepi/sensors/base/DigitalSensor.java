package com.dexterind.grovepi.sensors.base;

import java.io.IOException;

import com.dexterind.grovepi.*;
import com.dexterind.grovepi.utils.*;

public class DigitalSensor extends Sensor {
  protected int pin = 0;
  protected Debug debug;

  public DigitalSensor(int pin) throws IOException, InterruptedException, Exception {
	super();
	this.pin = pin;
  }
  
  public byte[] readBytes() throws IOException {
	this.board.writeI2c(Commands.DREAD, this.pin, Commands.UNUSED, Commands.UNUSED);
	return this.board.readI2c(1);
  }
  
  public boolean write(int value) throws IOException {
	this.board.writeI2c(Commands.DWRITE, this.pin, value, Commands.UNUSED);
	return true;
  }
}
