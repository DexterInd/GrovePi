package com.dexterind.grovepi.sensors;

import java.io.IOException;
import java.math.BigInteger;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.util.Arrays;

import com.dexterind.grovepi.*;
import com.dexterind.grovepi.sensors.base.*;
import com.dexterind.grovepi.utils.*;

public class DHTDigitalSensor extends DigitalSensor {
  private int moduleType = 0;
  private int scale = 0;
  
  private Debug debug;

  public static final int MODULE_DHT11 = 0;
  public static final int MODULE_DHT22 = 1;
  public static final int MODULE_DHT21 = 2;
  public static final int MODULE_AM2301 = 3;
  
  public static final int SCALE_C = 0;
  public static final int SCALE_F = 1;
  
  private byte[] bytes;
  
  private float convertCtoF(double temp) {
	  return (float) temp * 9 / 5 + 32;
  }
  
  private float convertFtoC(double temp) {
	  return (float) ((temp - 32) * 5 / 9);
  }
  
  private float getHeatIndex(float temp, float hum, int scale) {
	  boolean needsConversion = scale == DHTDigitalSensor.SCALE_C;
	  temp = needsConversion ? this.convertCtoF(temp) : temp;
	  
	  double hi = -42.379 +
		           2.04901523  * temp +
		           10.14333127 * hum +
		          -0.22475541  * temp * hum +
		          -0.00683783  * Math.pow(temp, 2) +
		          -0.05481717  * Math.pow(hum, 2) +
		           0.00122874  * Math.pow(temp, 2) * hum +
		           0.00085282  * temp * Math.pow(hum, 2) +
		          -0.00000199  * Math.pow(temp, 2) * Math.pow(hum, 2);
		  
	  return (float) (needsConversion ? this.convertFtoC(hi) : hi);
  }

  public DHTDigitalSensor(int pin, int moduleType, int scale) throws IOException, InterruptedException, Exception {
	super(pin);
	this.moduleType = moduleType;
	this.scale = scale;
  }
  
  private void storeBytes() throws IOException {
	this.board.writeI2c(Commands.DHT_TEMP, this.pin, this.moduleType, Commands.UNUSED);
	this.board.sleep(500);
	
	this.board.readI2c(1);
	this.board.sleep(200);
	
	this.bytes = this.board.readI2c(9);
  }

  public float[] read() {
	try {
		this.storeBytes();
	} catch(IOException e) {
		System.err.println("IOException: " + e.getMessage());
	}
	
	float temp = ByteBuffer.wrap(this.bytes).order(ByteOrder.LITTLE_ENDIAN).getFloat(1);
	float hum = ByteBuffer.wrap(this.bytes).order(ByteOrder.LITTLE_ENDIAN).getFloat(5);
	float heatIndex = this.getHeatIndex(temp, hum, this.scale);
	
	return new float[]{temp, hum , heatIndex};
  }
}
