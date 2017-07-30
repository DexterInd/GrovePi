package com.dexterind.grovepi.sensors.base;

import java.io.IOException;

import com.dexterind.grovepi.*;
import com.dexterind.grovepi.utils.*;

public class AnalogSensor extends Sensor {
  protected int pin = 0;
  private int length = 4;

  protected Debug debug;

  public AnalogSensor(int pin, int length) throws IOException, InterruptedException, Exception {
	super();
	this.pin = pin;
	this.length = length == -1 ? this.length : length;
  }
  
  public byte[] readBytes() throws IOException {
	this.board.writeI2c(Commands.AREAD, this.pin, Commands.UNUSED, Commands.UNUSED);
	this.board.readI2c(1);
	return this.board.readI2c(this.length);
  }
  
  public boolean write(int value) throws IOException {
	this.board.writeI2c(Commands.AWRITE, this.pin, value, Commands.UNUSED);
	return true;
  }
}
